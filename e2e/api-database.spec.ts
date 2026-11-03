import { test, expect } from "@playwright/test";

test("backend health endpoint is available", async ({ request }) => {
  const response = await request.get("/api/health");
  expect(response.ok()).toBeTruthy();
  await expect(response.json()).resolves.toMatchObject({
    status: "ok",
    service: "qalqan-api"
  });
});

test("PostgreSQL is connected and schema migrations are applied", async ({ request }) => {
  const response = await request.get("/api/ready");
  expect(response.status()).toBe(200);
  await expect(response.json()).resolves.toMatchObject({
    status: "ready",
    database: "connected",
    migrations: "applied"
  });
});
