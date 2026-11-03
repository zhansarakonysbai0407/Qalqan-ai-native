import { test, expect } from "@playwright/test";

test("language selector switches the interface to Russian", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("combobox", { name: "Language" }).selectOption("ru");
  await expect(page.getByRole("heading", { name: "Ваша безопасность важна" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Активировать SOS" })).toBeVisible();
});

test("language selector switches the interface to Kazakh", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("combobox", { name: "Language" }).selectOption("kk");
  await expect(page.getByRole("heading", { name: "Сіздің қауіпсіздігіңіз маңызды" })).toBeVisible();
  await expect(page.getByRole("button", { name: "SOS іске қосу" })).toBeVisible();
});
