import { test, expect } from "@playwright/test";

test("SOS confirmation can be cancelled without activating the demo", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /activate sos/i }).click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await page.getByRole("button", { name: "Cancel" }).click();
  await expect(page.getByRole("dialog")).toHaveCount(0);
  await expect(page.getByRole("status")).toHaveCount(0);
});

test("SOS confirmation displays a clear demo-only notice", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /activate sos/i }).click();
  await page.getByRole("button", { name: /confirm \(demo\)/i }).click();
  await expect(page.getByRole("status")).toContainText(/demo only/i);
  await expect(page.getByText(/no message is sent to contacts or emergency services/i)).toBeVisible();
});
