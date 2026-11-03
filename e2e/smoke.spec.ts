import { test, expect } from "@playwright/test";

test("Qalqan home page loads and confirms the demo-only SOS state", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /your safety matters/i })).toBeVisible();
  await page.getByRole("button", { name: /activate sos/i }).click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await page.getByRole("button", { name: /confirm \(demo\)/i }).click();
  await expect(page.getByRole("status")).toContainText(/demo only/i);
});