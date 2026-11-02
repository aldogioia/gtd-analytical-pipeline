#!/usr/bin/env node
/** Build the web app and publish only dist/ to gh-pages, without touching main. */
import { spawnSync } from 'node:child_process';
import { cp, mkdtemp, readdir, readFile, rm, stat } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dist = path.join(root, 'gtd-story', 'dist');
const branch = 'gh-pages';
const domain = 'gtd.aldogioia.com';
const expectedRepository = 'https://github.com/aldogioia/gtd-analytical-pipeline.git';
const dryRun = process.argv.includes('--dry-run');
if (process.argv.slice(2).some((arg) => arg !== '--dry-run'))
  throw Error('Usage: npm run deploy [-- --dry-run]');

function run(command, args, cwd = root, { capture = false, allowFailure = false } = {}) {
  const result = spawnSync(command, args, {
    cwd,
    encoding: 'utf8',
    stdio: capture ? 'pipe' : 'inherit',
  });
  if (result.error) throw result.error;
  if (result.status !== 0 && !allowFailure)
    throw Error(
      `${command} ${args.join(' ')} failed (${result.status}).${capture ? '\n' + result.stderr : ''}`,
    );
  return { code: result.status, output: result.stdout?.trim() || '' };
}
async function validateBuild(directory) {
  for (const file of [
    'index.html',
    'CNAME',
    '.nojekyll',
    'data/story.json',
    'data/locations.json',
    'data/map-locations.json',
  ])
    await stat(path.join(directory, file));
  if ((await readFile(path.join(directory, 'CNAME'), 'utf8')).trim() !== domain)
    throw Error('CNAME does not match the intended subdomain.');
  const forbidden = new Set([
    '.git',
    'node_modules',
    'Presentation & Report',
    'DWV.pdf',
    'GTD_Data_Storytelling.pdf',
  ]);
  async function walk(dir) {
    for (const entry of await readdir(dir, { withFileTypes: true })) {
      if (forbidden.has(entry.name))
        throw Error(`Private or source material in build: ${entry.name}`);
      const full = path.join(dir, entry.name);
      if (entry.isSymbolicLink()) throw Error(`Unexpected symlink: ${full}`);
      if (entry.isDirectory()) await walk(full);
      else if ((await stat(full)).size >= 100 * 1024 * 1024)
        throw Error(`Asset exceeds GitHub's file limit: ${full}`);
    }
  }
  await walk(directory);
}

let checkout;
try {
  run('npm', ['run', 'build']);
  await validateBuild(dist);
  if (dryRun) {
    console.log(`Build verified for https://${domain}. Branch: ${branch}. No Git push performed.`);
    process.exitCode = 0;
  } else {
    const repository = run('git', ['remote', 'get-url', 'origin'], root, { capture: true }).output;
    if (repository.replace(/\.git$/, '') !== expectedRepository.replace(/\.git$/, ''))
      throw Error('origin is not the expected GTD repository. Update it before deploying.');
    checkout = await mkdtemp(path.join(tmpdir(), 'gtd-pages-'));
    run('git', ['init', '--initial-branch', branch], checkout, { capture: true });
    run('git', ['remote', 'add', 'origin', repository], checkout);
    const remote = run(
      'git',
      ['ls-remote', '--exit-code', '--heads', 'origin', `refs/heads/${branch}`],
      checkout,
      { capture: true, allowFailure: true },
    );
    if (remote.code === 0) {
      run('git', ['fetch', '--depth=1', 'origin', branch], checkout);
      run('git', ['checkout', '-B', branch, 'FETCH_HEAD'], checkout, { capture: true });
    } else if (remote.code !== 2)
      throw Error(
        'Cannot read the remote publishing branch. Check GitHub authentication and network access.',
      );
    for (const entry of await readdir(checkout))
      if (entry !== '.git') await rm(path.join(checkout, entry), { recursive: true, force: true });
    await cp(dist, checkout, { recursive: true });
    const name =
      run('git', ['config', 'user.name'], root, { capture: true, allowFailure: true }).output ||
      'GitHub Pages';
    const email =
      run('git', ['config', 'user.email'], root, { capture: true, allowFailure: true }).output ||
      'pages@users.noreply.github.com';
    run('git', ['config', 'user.name', name], checkout);
    run('git', ['config', 'user.email', email], checkout);
    run('git', ['add', '--all', '--', '.'], checkout);
    const difference = run('git', ['diff', '--cached', '--quiet'], checkout, {
      capture: true,
      allowFailure: true,
    });
    if (difference.code === 1) {
      const source = run('git', ['rev-parse', '--short', 'HEAD'], root, { capture: true }).output;
      run('git', ['commit', '-m', `Deploy GTD story from ${source}`], checkout, { capture: true });
      // Normal push deliberately rejects concurrent updates; deployment never force-pushes.
      run('git', ['push', 'origin', `HEAD:refs/heads/${branch}`], checkout);
      console.log(`Published build to ${branch}. Site: https://${domain}`);
    } else if (difference.code === 0) console.log('The published build is already up to date.');
    else throw Error('Cannot inspect the staged publishing build.');
  }
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
} finally {
  if (checkout) await rm(checkout, { recursive: true, force: true });
}
