const { test, expect } = require('@playwright/test');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { pathToFileURL } = require('node:url');

test.beforeEach(async ({ context }) => {
  await context.addInitScript(()=>{window.CODELAB_DISABLE_MONACO=true;window.CODELAB_DISABLE_PYTHON=true;});
  await context.addInitScript(() => { try { localStorage.setItem('cl_first_visit', 'false'); } catch {} });
  await context.route('**/*', route => {
    const url = new URL(route.request().url());
    if (url.hostname !== '127.0.0.1' && url.protocol !== 'file:') return route.abort();
    return route.continue();
  });
});

test('generated packs are complete and internally consistent', async () => {
  const box = { window: { CODELAB_OFFLINE_PACKS: {} } };
  vm.runInNewContext(fs.readFileSync('offline/catalog.js', 'utf8'), box);
  const catalog = box.window.CODELAB_OFFLINE_CATALOG;
  for (const file of catalog.files) expect(fs.existsSync(path.resolve(file)), file).toBe(true);
  for (const file of catalog.files.filter(f => f.endsWith('.js'))) vm.runInNewContext(fs.readFileSync(file, 'utf8'), box);
  const records = Object.values(box.window.CODELAB_OFFLINE_PACKS);
  expect(records.length).toBe(catalog.stats.entries);
  expect(new Set(catalog.entries.map(e => e.key)).size).toBe(catalog.entries.length);
  expect(records.reduce((n,r) => n + r.solutions.length, 0)).toBe(catalog.stats.solutions);
  expect(records.reduce((n,r) => n + r.documents.length, 0)).toBe(catalog.stats.documents);
  for (const entry of catalog.entries) {
    const r = box.window.CODELAB_OFFLINE_PACKS[entry.key];
    expect(r.title).toBe(entry.title);
    expect(r.solutions.length).toBe(entry.solutionCount);
    expect(new Set(r.solutions.map(s => s.hash)).size).toBe(r.solutions.length);
  }
});

test('filters, bookmarks, pagination and saved review state', async ({ page }) => {
  const errors = []; page.on('pageerror', e => errors.push(e.message));
  await page.goto('/');
  await page.getByRole('button', { name: '📚 Offline Library', exact:true }).click();
  await expect(page.getByRole('heading', {name:'Offline Library', exact:true})).toBeVisible();
  await expect(page.locator('.lib-table tbody tr')).toHaveCount(40);
  await page.getByRole('button', {name:'Next →',exact:true}).click();
  await expect(page.locator('#lib-pagination')).toContainText('41–80');
  await page.getByRole('searchbox', {name:'Search offline library'}).fill('one edit distance');
  await page.getByRole('combobox', {name:'Filter source'}).selectOption('complete');
  await page.getByRole('combobox', {name:'Filter difficulty'}).selectOption('Medium');
  await page.getByRole('combobox', {name:'Filter language'}).selectOption('cpp');
  await expect(page.locator('.lib-table tbody tr')).toHaveCount(1);
  await page.getByRole('button', {name:'Bookmark One Edit Distance',exact:true}).click();
  await page.getByRole('button', {name:'161. One Edit Distance',exact:true}).click();
  await expect(page.getByRole('heading', {name:'161. One Edit Distance',exact:true})).toBeVisible();
  await expect(page.locator('#lib-reading')).toContainText('exactly one');
  await page.getByRole('button', {name:'Mark reviewed',exact:true}).click();
  expect(await page.evaluate(() => Progress.solved())).toEqual([]);
  await page.getByRole('button', {name:'← Back to library',exact:true}).click();
  await page.getByRole('combobox', {name:'Filter progress'}).selectOption('reviewed');
  await expect(page.locator('.lib-table tbody tr')).toHaveCount(1);
  await page.getByRole('combobox', {name:'Filter language'}).selectOption('rust');
  await expect(page.getByText('No matches.',{exact:false})).toBeVisible();
  await page.getByRole('combobox', {name:'Filter language'}).selectOption('');
  await expect(page.locator('.lib-table tbody tr')).toHaveCount(1);
  expect(errors).toEqual([]);
});

test('downloaded folder opens directly without an HTTP server', async ({ page }) => {
  await page.goto(pathToFileURL(path.resolve('index.html')).href + '#library/lc-161');
  await expect(page.getByRole('heading', {name:'161. One Edit Distance',exact:true})).toBeVisible();
  await expect(page.locator('#lib-reading')).toContainText('exactly one');
  await page.getByRole('tab',{name:/Solutions/}).click();
  await expect(page.locator('.lib-code')).toContainText('class Solution');
});

test('deep links, multiple languages, draft persistence and progress backup', async ({ page }) => {
  await page.goto('/#library/lc-100');
  await expect(page.getByRole('heading', {name:'100. Same Tree',exact:true})).toBeVisible();
  await page.getByRole('tab', {name:/Solutions/}).click();
  await expect(page.locator('#lib-solution')).toBeVisible();
  const values = await page.locator('#lib-solution option').allTextContents();
  expect(values.some(v => v.includes('Python'))).toBe(true);
  expect(values.some(v => v.includes('C++'))).toBe(true);
  await page.locator('#lib-solution').selectOption('1');
  await expect(page.locator('.lib-code')).not.toBeEmpty();
  await page.getByRole('tab', {name:'My workspace',exact:true}).click();
  await page.locator('#lib-draft').fill('my solution <script>never executed</script>');
  await page.locator('#lib-notes').fill('Check empty trees');
  await page.reload();
  await page.getByRole('tab', {name:'My workspace',exact:true}).click();
  await expect(page.locator('#lib-draft')).toHaveValue('my solution <script>never executed</script>');
  await expect(page.locator('#lib-notes')).toHaveValue('Check empty trees');
  const downloaded = page.waitForEvent('download');
  await page.evaluate(() => DataIO.exportProgress());
  const file = await (await downloaded).path();
  const backup = JSON.parse(fs.readFileSync(file, 'utf8'));
  expect(backup._raw['cl_library_notes_lc-100']).toBe('Check empty trees');
  await page.evaluate(() => { localStorage.removeItem('cl_library_notes_lc-100'); });
  const chooser = page.waitForEvent('filechooser');
  await page.evaluate(() => DataIO.importProgress());
  await (await chooser).setFiles({name:'progress.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(backup))});
  await expect.poll(() => page.evaluate(() => localStorage.getItem('cl_library_notes_lc-100'))).toBe('Check empty trees');
});

test('imported documents are sanitized without remote image requests', async ({ page }) => {
  await page.goto('/#library/lc-1');
  await expect(page.getByRole('heading', {name:'1. Two Sum',exact:true})).toBeVisible();
  await expect(page.locator('#lib-reading')).not.toContainText('??? Show');
  await expect(page.locator('#lib-reading')).not.toContainText('--8<--');
  await page.evaluate(() => {
    OfflineLibrary.selected.documents = [{source:'primer',path:'test.md',text:'<script>window.__pwn=1</script><img src="https://evil.invalid/track" onerror="window.__pwn=2"><a href="javascript:alert(1)">unsafe</a><p onclick="window.__pwn=3">safe text</p>'}];
    OfflineLibrary.documentIndex = 0; OfflineLibrary.reader();
  });
  await expect(page.locator('#lib-reading script')).toHaveCount(0);
  await expect(page.locator('#lib-reading img')).toHaveCount(0);
  await expect(page.locator('#lib-reading [onclick]')).toHaveCount(0);
  await expect(page.locator('#lib-reading a')).not.toHaveAttribute('href');
  expect(await page.evaluate(() => window.__pwn)).toBeUndefined();
});

test('complete library survives offline reload including unread packs and diagrams', async ({ context, page }) => {
  await page.goto('/#library');
  await page.getByRole('button', {name:'Save for offline',exact:true}).click();
  await expect(page.locator('#lib-cache-status')).toContainText('Ready offline.', {timeout:60000});
  await context.setOffline(true);
  const offline = await context.newPage();
  await offline.goto('http://127.0.0.1:4193/#library/lc-156');
  await expect(offline.getByRole('heading', {name:'156. Binary Tree Upside Down',exact:true})).toBeVisible();
  await expect(offline.locator('#lib-reading')).toContainText('Constraints:');
  const img = offline.locator('#lib-reading img').first();
  await img.scrollIntoViewIfNeeded();
  await expect.poll(() => img.evaluate(el => el.complete && el.naturalWidth > 0)).toBe(true);
  await offline.getByRole('tab',{name:/Solutions/}).click();
  await expect(offline.locator('.lib-code')).toContainText('class Solution');
});

test('mobile library has no horizontal page overflow', async ({ page }) => {
  await page.setViewportSize({width:390,height:844});
  await page.goto('/#library');
  await expect(page.getByRole('heading',{name:'Offline Library',exact:true})).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await page.screenshot({path:'test-results/library-mobile.png',fullPage:true});
});
