"use client";

import { Suspense, useEffect, useState } from "react";
import { signIn, useSession } from "next-auth/react";
import { useSearchParams } from "next/navigation";

function LoginForm() {
  const { status } = useSession();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl") ?? "/";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (status === "authenticated") {
      window.location.assign(callbackUrl);
    }
  }, [status, callbackUrl]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const res = await signIn("credentials", {
      email,
      password,
      redirect: false,
      callbackUrl,
    });
    setLoading(false);
    if (res?.error) {
      setError("Invalid email or password.");
      return;
    }
    if (res?.ok && res.url) {
      window.location.assign(res.url);
    }
  }

  return (
    <div className="flex min-h-dvh items-center justify-center bg-[var(--bg)] p-6">
      <div className="w-full max-w-[380px] rounded-[var(--radius-lg)] border border-[var(--border)] bg-[var(--panel)] p-8 shadow-[var(--shadow-float)]">
        <div className="ds-aside-stack mb-6">
          <div className="ds-brand-title">UPTOWNS</div>
          <div className="ds-brand-sub">Sign in to continue</div>
        </div>

        <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
          <label className="flex flex-col gap-1.5">
            <span className="text-[var(--text-xs)] font-medium uppercase tracking-[var(--tracking-overline)] text-[var(--muted)]">
              Email
            </span>
            <input
              name="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="ds-input w-full"
            />
          </label>
          <label className="flex flex-col gap-1.5">
            <span className="text-[var(--text-xs)] font-medium uppercase tracking-[var(--tracking-overline)] text-[var(--muted)]">
              Password
            </span>
            <input
              name="password"
              type="password"
              autoComplete="current-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="ds-input w-full"
            />
          </label>

          {error ? (
            <p className="rounded-[var(--radius-sm)] border border-[var(--danger)]/40 bg-[var(--danger)]/10 px-3 py-2 text-[var(--text-xs)] text-[var(--danger)]">
              {error}
            </p>
          ) : null}

          <button type="submit" className="ds-btn-primary w-full py-2.5" disabled={loading}>
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-dvh items-center justify-center bg-[var(--bg)] text-[var(--text-secondary)]">
          Loading…
        </div>
      }
    >
      <LoginForm />
    </Suspense>
  );
}
