import {
  afterEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllEnvs();
  vi.unstubAllGlobals();
  vi.resetModules();
});

describe("API error handling", () => {
  it("surfaces server failures", async () => {
    vi.stubEnv("VITE_DEMO_MODE", "false");
    vi.resetModules();

    const { apiGet } = await import("./api");

    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            detail: "Backend unavailable",
          }),
          {
            status: 503,
            headers: {
              "Content-Type": "application/json",
            },
          },
        ),
      ),
    );

    await expect(apiGet("/records")).rejects.toThrow(
      "Backend unavailable",
    );
  });

  it("reports invalid JSON payloads", async () => {
    vi.stubEnv("VITE_DEMO_MODE", "false");
    vi.resetModules();

    const { apiGet, ApiError } = await import("./api");

    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response("nope", {
          status: 200,
        }),
      ),
    );

    await expect(apiGet("/records")).rejects.toThrow(
      ApiError,
    );
  });
});