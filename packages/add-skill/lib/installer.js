const degit = require("degit");
const path = require("path");
const fs = require("fs");

const TIMEOUT_MS = 60000; // 60 second timeout for downloads

// Only these directories get installed to .claude/
const INSTALL_DIRS = ["agents", "commands", "hooks", "skills"];

/**
 * Validate GitHub repository format
 * @param {string} repo - Repository string to validate
 * @returns {boolean} True if valid format
 */
function isValidRepoFormat(repo) {
  // Must be "owner/repo" format with safe characters only
  // Allows: letters, numbers, hyphens, underscores, dots
  return /^[\w.-]+\/[\w.-]+$/.test(repo);
}

/**
 * Install a Claude Code plugin from GitHub (additive merge)
 * @param {string} repo - GitHub repo in format "owner/repo"
 * @param {string} name - Plugin name for display
 * @throws {Error} If plugin already installed or download fails
 */
async function install(repo, name) {
  // HIGH-1 FIX: Validate repository format to prevent path traversal
  if (!isValidRepoFormat(repo)) {
    throw new Error(
      `Invalid repository format: "${repo}". Expected: owner/repo`,
    );
  }

  const cwd = process.cwd();
  const target = path.join(cwd, ".claude");
  // MEDIUM-1 FIX: Use PID-based temp directory to prevent race conditions
  const tempTarget = path.join(cwd, `.claude-temp-install-${process.pid}`);

  const hasExisting = fs.existsSync(target);
  if (hasExisting) {
    console.log(`\n📁 Found existing .claude/ - will merge (nothing deleted)`);
  }

  console.log(`\n📦 Installing ${name}...`);

  // Clean up any previous failed install
  if (fs.existsSync(tempTarget)) {
    fs.rmSync(tempTarget, { recursive: true, force: true });
  }

  // Download to temp directory with timeout and error handling
  const emitter = degit(repo, {
    cache: false,
    force: true,
    verbose: false,
  });

  let timeoutId;
  try {
    const timeoutPromise = new Promise((_, reject) => {
      timeoutId = setTimeout(
        () => reject(new Error("Download timed out after 60 seconds")),
        TIMEOUT_MS,
      );
    });
    await Promise.race([emitter.clone(tempTarget), timeoutPromise]);
    clearTimeout(timeoutId);
  } catch (err) {
    clearTimeout(timeoutId);
    // Clean up temp on failure
    if (fs.existsSync(tempTarget)) {
      fs.rmSync(tempTarget, { recursive: true, force: true });
    }
    // MEDIUM-3 FIX: Enhanced error messages with actionable context
    if (err.code === "ENOTFOUND" || err.message.includes("getaddrinfo")) {
      throw new Error(
        `Network error accessing github.com/${repo}\n` +
          `   Check: internet connection, firewall, proxy settings`,
      );
    }
    if (err.message.includes("could not find commit")) {
      throw new Error(
        `Repository not found: github.com/${repo}\n` +
          `   Verify the repository exists and is public`,
      );
    }
    throw new Error(`Download failed for ${repo}: ${err.message}`);
  }

  // Create target if it doesn't exist
  if (!fs.existsSync(target)) {
    fs.mkdirSync(target, { recursive: true });
  }

  // Merge: copy only agents, commands, hooks, skills to target
  const stats = { added: 0, skipped: 0 };
  for (const dir of INSTALL_DIRS) {
    const srcDir = path.join(tempTarget, dir);
    const destDir = path.join(target, dir);
    if (fs.existsSync(srcDir)) {
      if (!fs.existsSync(destDir)) {
        fs.mkdirSync(destDir, { recursive: true });
      }
      mergeDirectories(srcDir, destDir, stats);
    }
  }

  // Clean up temp
  fs.rmSync(tempTarget, { recursive: true, force: true });

  const hookResult = registerHooks(target);

  // Count installed components
  const components = {
    agents: countFiles(path.join(target, "agents"), ".md"),
    skills: countDirs(path.join(target, "skills")),
    commands: countFiles(path.join(target, "commands"), ".md"),
    hooks:
      countFiles(path.join(target, "hooks"), ".py") +
      countFiles(path.join(target, "hooks"), ".sh"),
  };

  console.log(`\n✅ Installed to .claude/\n`);
  console.log(
    `   ${components.agents} agents | ${components.skills} skills | ${components.commands} commands | ${components.hooks} hooks`,
  );
  if (hookResult.added > 0) {
    console.log(
      `   ${hookResult.added} hooks registered in .claude/settings.json`,
    );
  } else if (hookResult.error) {
    console.log(
      `   ⚠️  Hooks were copied but NOT registered: ${hookResult.error}`,
    );
    console.log(
      `      Add them to .claude/settings.json manually (see .claude/hooks/hooks.json).`,
    );
  } else if (hookResult.present > 0) {
    console.log(`   Hooks already registered in .claude/settings.json`);
  }
  if (stats.skipped > 0) {
    console.log(`   (${stats.skipped} existing files preserved)`);
  }
  console.log(`\n   Run 'claude' to start.`);
}

/**
 * Check whether a value is a plain (non-array, non-null) object
 */
function isPlainObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

/**
 * Register the copied hooks in <target>/settings.json (additive, idempotent).
 * Claude Code ignores .claude/hooks/hooks.json, so the hooks never run otherwise.
 * @param {string} target - Absolute path of the .claude directory
 * @returns {{added: number, present: number, error: string|null}} Never throws
 */
function registerHooks(target) {
  const none = { added: 0, present: 0, error: null };
  try {
    let source;
    try {
      source = JSON.parse(
        fs.readFileSync(path.join(target, "hooks", "hooks.json"), "utf8"),
      );
    } catch {
      return none;
    }
    if (!isPlainObject(source) || !isPlainObject(source.hooks)) return none;

    const settingsPath = path.join(target, "settings.json");
    let settings = {};
    if (fs.existsSync(settingsPath)) {
      try {
        settings = JSON.parse(fs.readFileSync(settingsPath, "utf8"));
      } catch {
        return {
          added: 0,
          present: 0,
          error: "settings.json is not valid JSON",
        };
      }
      if (!isPlainObject(settings)) {
        return {
          added: 0,
          present: 0,
          error: "settings.json is not a JSON object",
        };
      }
    }
    if (settings.hooks !== undefined && !isPlainObject(settings.hooks)) {
      return {
        added: 0,
        present: 0,
        error: '"hooks" in settings.json is not an object',
      };
    }
    for (const event of Object.keys(source.hooks)) {
      if (
        settings.hooks &&
        settings.hooks[event] !== undefined &&
        !Array.isArray(settings.hooks[event])
      ) {
        return {
          added: 0,
          present: 0,
          error: `hooks.${event} in settings.json is not an array`,
        };
      }
    }

    let added = 0;
    let present = 0;
    for (const [event, groups] of Object.entries(source.hooks)) {
      if (!Array.isArray(groups)) continue;
      const known = new Set();
      const existing = settings.hooks ? settings.hooks[event] || [] : [];
      for (const group of existing) {
        if (!isPlainObject(group) || !Array.isArray(group.hooks)) continue;
        for (const h of group.hooks) {
          if (isPlainObject(h) && typeof h.command === "string") {
            known.add(h.command);
          }
        }
      }

      for (const group of groups) {
        if (!isPlainObject(group) || !Array.isArray(group.hooks)) continue;
        const fresh = [];
        for (const h of group.hooks) {
          if (!isPlainObject(h) || typeof h.command !== "string") continue;
          let missing = false;
          let scripts = 0;
          // Replacer function: a string replacement would treat "$C"/"$1" specially
          const command = h.command.replace(
            /"?\$\{CLAUDE_PLUGIN_ROOT\}\/hooks\/([\w.-]+)"?/g,
            (_, name) => {
              scripts++;
              const script = path.join(target, "hooks", name);
              if (!fs.existsSync(script) || !fs.statSync(script).isFile()) {
                missing = true;
              }
              return `"$CLAUDE_PROJECT_DIR/.claude/hooks/${name}"`;
            },
          );
          // Only register commands that run a hook script we actually copied
          if (missing || scripts === 0) continue;
          if (known.has(command)) {
            present++;
            continue;
          }
          known.add(command);
          fresh.push({ ...h, command });
        }
        if (fresh.length === 0) continue;
        const entry = {};
        if (group.matcher !== undefined) entry.matcher = group.matcher;
        entry.hooks = fresh;
        if (!settings.hooks) settings.hooks = {};
        if (!settings.hooks[event]) settings.hooks[event] = [];
        settings.hooks[event].push(entry);
        added += fresh.length;
      }
    }

    if (added > 0) {
      fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + "\n");
    }
    return { added, present, error: null };
  } catch (err) {
    return { added: 0, present: 0, error: err.message };
  }
}

/**
 * Recursively merge source directory into target, preserving existing files
 * Handles regular files, directories, and symlinks
 */
function mergeDirectories(src, dest, stats) {
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isSymbolicLink()) {
      // HIGH-2 FIX: Validate symlink targets to prevent path traversal attacks
      if (!fs.existsSync(destPath)) {
        const linkTarget = fs.readlinkSync(srcPath);
        const resolvedTarget = path.resolve(path.dirname(destPath), linkTarget);
        const resolvedDest = path.resolve(dest);

        // Only allow symlinks that point inside the .claude directory
        if (
          !resolvedTarget.startsWith(resolvedDest + path.sep) &&
          resolvedTarget !== resolvedDest
        ) {
          // Unsafe symlink - skip it with warning
          console.warn(
            `   ⚠️  Skipping unsafe symlink: ${entry.name} -> ${linkTarget}`,
          );
          stats.skipped++;
          continue;
        }

        fs.symlinkSync(linkTarget, destPath);
        stats.added++;
      } else {
        stats.skipped++;
      }
    } else if (entry.isDirectory()) {
      // Create directory if it doesn't exist
      if (!fs.existsSync(destPath)) {
        fs.mkdirSync(destPath, { recursive: true });
      }
      // Recursively merge
      mergeDirectories(srcPath, destPath, stats);
    } else if (entry.isFile()) {
      // Only copy file if it doesn't exist in destination
      if (!fs.existsSync(destPath)) {
        fs.copyFileSync(srcPath, destPath);
        stats.added++;
      } else {
        stats.skipped++;
      }
    }
    // Skip other types (sockets, fifos, etc.)
  }
}

/**
 * Count files with a specific extension in a directory
 */
function countFiles(dir, ext) {
  try {
    if (!fs.existsSync(dir)) return 0;
    return fs.readdirSync(dir).filter((f) => f.endsWith(ext)).length;
  } catch {
    return 0;
  }
}

/**
 * Count subdirectories in a directory
 */
function countDirs(dir) {
  try {
    if (!fs.existsSync(dir)) return 0;
    return fs
      .readdirSync(dir, { withFileTypes: true })
      .filter((d) => d.isDirectory()).length;
  } catch {
    return 0;
  }
}

module.exports = { install, registerHooks };
