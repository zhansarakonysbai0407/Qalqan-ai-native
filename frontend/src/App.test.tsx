import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "./App";

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("Qalqan landing page", () => {
  it("shows the safety introduction and SOS action", () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({ status: "ok" }) })));
    render(<App />);
    expect(screen.getByRole("heading", { name: /your safety matters/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /activate sos/i })).toBeInTheDocument();
  });

  it("requires confirmation before showing the demo action", async () => {
    const user = userEvent.setup();
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({ status: "ok" }) })));
    render(<App />);
    await user.click(screen.getByRole("button", { name: /activate sos/i }));
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: /confirm \\(demo\\)/i }));
    expect(screen.getByRole("status")).toHaveTextContent(/demo only/i);
  });
});
