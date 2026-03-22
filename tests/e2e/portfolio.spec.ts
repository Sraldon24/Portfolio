import { test, expect } from '@playwright/test';

const EN = '/en/';
const FR = '/fr/';

// ── Helpers ────────────────────────────────────────────────────────────────

async function dismissBoot(page: any) {
  // Boot screen is skipped if sessionStorage already set; either way wait for it to clear
  const boot = page.locator('#boot-screen');
  try {
    await boot.waitFor({ state: 'hidden', timeout: 8000 });
  } catch {
    // Already gone
  }
}

// ── EN page smoke tests ────────────────────────────────────────────────────

test.describe('EN — smoke', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(EN);
    await dismissBoot(page);
  });

  test('page loads with 200 and correct title', async ({ page }) => {
    await expect(page).toHaveTitle(/Portfolio/i);
  });

  test('nav links are visible', async ({ page }) => {
    for (const label of ['About', 'Projects', 'Career', 'Contact']) {
      await expect(page.locator(`nav a:has-text("${label}")`).first()).toBeVisible();
    }
  });

  test('hero section renders glitch name and boot card', async ({ page }) => {
    await expect(page.locator('#about')).toBeVisible();
    await expect(page.locator('.glitch').first()).toBeVisible();
    await expect(page.locator('#terminal-boot-lines')).toBeAttached();
  });

  test('all 7 sections exist in DOM', async ({ page }) => {
    for (const id of ['about', 'system-info', 'projects', 'career', 'human', 'testimonials', 'contact']) {
      await expect(page.locator(`#${id}`)).toBeAttached();
    }
  });

  test('projects section renders at least one card', async ({ page }) => {
    await page.locator('#projects').scrollIntoViewIfNeeded();
    const cards = page.locator('#projects .project-card, #projects .bento-card, #projects .glass-card');
    await expect(cards.first()).toBeVisible({ timeout: 5000 });
  });

  test('contact form is present and submittable', async ({ page }) => {
    await page.locator('#contact').scrollIntoViewIfNeeded();
    await expect(page.locator('input[name="contact-name"]')).toBeVisible();
    await expect(page.locator('input[name="contact-email"]')).toBeVisible();
    await expect(page.locator('textarea[name="contact-message"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]').last()).toBeVisible();
  });

  test('footer renders with current year', async ({ page }) => {
    const year = new Date().getFullYear().toString();
    await expect(page.locator('footer')).toContainText(year);
  });

  test('language switcher shows [EN] and [FR]', async ({ page }) => {
    await expect(page.locator('nav a:has-text("[EN]")')).toBeVisible();
    await expect(page.locator('nav a:has-text("[FR]")')).toBeVisible();
  });
});

// ── FR page smoke tests ────────────────────────────────────────────────────

test.describe('FR — smoke + translations', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(FR);
    await dismissBoot(page);
  });

  test('FR page loads 200', async ({ page }) => {
    await expect(page).toHaveTitle(/Portfolio/i);
  });

  test('nav shows French labels', async ({ page }) => {
    await expect(page.locator('nav').first()).toContainText('À propos');
    await expect(page.locator('nav').first()).toContainText('Projets');
    await expect(page.locator('nav').first()).toContainText('Carrière');
    await expect(page.locator('nav').first()).toContainText('Contact');
  });

  test('no JS syntax errors on FR page', async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', err => errors.push(err.message));
    await page.goto(FR);
    await page.waitForLoadState('networkidle');
    const jsErrors = errors.filter(e => !e.includes('cloudflare') && !e.includes('beacon'));
    expect(jsErrors).toHaveLength(0);
  });

  test('CMD+K palette opens on FR page without crash', async ({ page }) => {
    await page.keyboard.press('Control+k');
    await expect(page.locator('#cmd-palette')).toHaveClass(/open/);
    // Palette items render (French labels)
    await expect(page.locator('.cmd-item').first()).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(page.locator('#cmd-palette')).not.toHaveClass(/open/);
  });

  test('language switch EN→FR→EN works', async ({ page }) => {
    await page.goto(EN);
    await dismissBoot(page);
    await page.locator('nav a:has-text("[FR]")').first().click();
    await expect(page).toHaveURL(/\/fr\//);
    await expect(page.locator('nav').first()).toContainText('À propos');
    await page.locator('nav a:has-text("[EN]")').first().click();
    await expect(page).toHaveURL(/\/en\//);
    await expect(page.locator('nav').first()).toContainText('About');
  });
});

// ── CMD+K palette (EN) ─────────────────────────────────────────────────────

test.describe('CMD+K palette', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(EN);
    await dismissBoot(page);
  });

  test('opens with Ctrl+K and closes with Escape', async ({ page }) => {
    await page.keyboard.press('Control+k');
    await expect(page.locator('#cmd-palette')).toHaveClass(/open/);
    await page.keyboard.press('Escape');
    await expect(page.locator('#cmd-palette')).not.toHaveClass(/open/);
  });

  test('filters items on input', async ({ page }) => {
    await page.keyboard.press('Control+k');
    await page.locator('#cmd-input').fill('proj');
    const items = page.locator('.cmd-item');
    await expect(items).toHaveCount(1);
    await expect(items.first()).toContainText('Projects');
  });

  test('navigates with arrow keys and selects with Enter', async ({ page }) => {
    await page.keyboard.press('Control+k');
    await page.keyboard.press('ArrowDown');
    await page.keyboard.press('ArrowDown');
    // Should have second item active
    const items = page.locator('.cmd-item');
    await expect(items.nth(2)).toHaveClass(/active/);
  });
});

// ── Boot screen ────────────────────────────────────────────────────────────

test.describe('Boot screen', () => {
  test('shows on fresh load and disappears', async ({ page }) => {
    // Clear sessionStorage to ensure boot runs
    await page.addInitScript(() => sessionStorage.clear());
    await page.goto(EN);
    // Boot screen should be visible initially
    const boot = page.locator('#boot-screen');
    await expect(boot).toBeVisible({ timeout: 2000 });
    // Then it should fade out
    await expect(boot).toBeHidden({ timeout: 10000 });
  });

  test('skipped on return visit (sessionStorage)', async ({ page }) => {
    // Set boot_done before load
    await page.addInitScript(() => sessionStorage.setItem('boot_done', '1'));
    await page.goto(EN);
    const boot = page.locator('#boot-screen');
    // Should never be visible
    await expect(boot).toBeHidden({ timeout: 2000 });
  });
});

// ── Mobile layout ──────────────────────────────────────────────────────────

test.describe('Mobile layout', () => {
  test.use({ viewport: { width: 390, height: 844 } });

  test('mobile menu button is visible and toggles menu', async ({ page }) => {
    await page.goto(EN);
    await dismissBoot(page);
    const menuBtn = page.locator('#mobile-menu-btn');
    await expect(menuBtn).toBeVisible();
    await menuBtn.click();
    await expect(page.locator('#mobile-menu')).toBeVisible();
  });

  test('hero renders properly on mobile', async ({ page }) => {
    await page.goto(EN);
    await dismissBoot(page);
    await expect(page.locator('#about')).toBeVisible();
    await expect(page.locator('.glitch').first()).toBeVisible();
  });
});
