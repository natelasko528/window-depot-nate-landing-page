(function ownerSharedScript() {
  "use strict";

  const REFRESH_MS = 60000;

  function el(selector) {
    return document.querySelector(selector);
  }

  function safeNumber(value) {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : 0;
  }

  function toPayload(data) {
    if (data && typeof data === "object" && "data" in data) {
      return data.data;
    }
    return data;
  }

  function errorMessage(data, fallback) {
    if (!data) {
      return fallback;
    }
    if (typeof data === "string") {
      return data;
    }
    if (typeof data.message === "string") {
      return data.message;
    }
    if (typeof data.error === "string") {
      return data.error;
    }
    return fallback;
  }

  function setStatus(target, message, type) {
    if (!target) {
      return;
    }
    target.textContent = message || "";
    target.classList.remove("error", "success");
    if (type) {
      target.classList.add(type);
    }
  }

  async function fetchJson(url, options) {
    const requestOptions = Object.assign(
      {
        method: "GET",
        credentials: "include",
        headers: {
          Accept: "application/json"
        }
      },
      options || {}
    );

    if (requestOptions.body && typeof requestOptions.body !== "string") {
      requestOptions.body = JSON.stringify(requestOptions.body);
      requestOptions.headers = Object.assign({}, requestOptions.headers, {
        "Content-Type": "application/json"
      });
    }

    try {
      const response = await fetch(url, requestOptions);
      const rawText = await response.text();
      let data = null;

      if (rawText) {
        try {
          data = JSON.parse(rawText);
        } catch (parseError) {
          data = { message: rawText };
        }
      }

      if (!response.ok) {
        return {
          ok: false,
          status: response.status,
          data: data,
          error: errorMessage(data, "Request failed")
        };
      }

      return {
        ok: true,
        status: response.status,
        data: data
      };
    } catch (networkError) {
      return {
        ok: false,
        status: 0,
        data: null,
        error: networkError.message || "Network error"
      };
    }
  }

  function formatNumber(value) {
    return new Intl.NumberFormat("en-US").format(safeNumber(value));
  }

  function formatPercent(value) {
    return safeNumber(value).toFixed(2) + "%";
  }

  function formatDate(value) {
    if (!value) {
      return "Never";
    }
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
      return "Never";
    }
    return date.toLocaleString();
  }

  function normalizeSession(payload) {
    const base = toPayload(payload);
    if (!base || typeof base !== "object") {
      return null;
    }

    const authenticated = base.authenticated === true ||
      base.sessionActive === true ||
      base.owner === true;

    if (authenticated) {
      return base;
    }

    if (base.user || base.email || base.name) {
      return Object.assign({ authenticated: true }, base);
    }

    return null;
  }

  async function checkSession(options) {
    const settings = Object.assign(
      {
        redirectIfUnauthed: true,
        redirectIfAuthed: false
      },
      options || {}
    );
    const response = await fetchJson("/api/auth/session");
    const normalized = response.ok ? normalizeSession(response.data) : null;

    if (normalized && settings.redirectIfAuthed) {
      window.location.replace("/owner/dashboard");
      return normalized;
    }

    if (!normalized && settings.redirectIfUnauthed) {
      window.location.replace("/owner");
      return null;
    }

    return normalized;
  }

  async function logout() {
    await fetchJson("/api/auth/logout", { method: "POST" });
    window.location.replace("/owner");
  }

  function attachLogoutHandler() {
    const logoutButton = el("#logoutButton");
    if (!logoutButton) {
      return;
    }
    logoutButton.addEventListener("click", function onLogoutClick() {
      logout();
    });
  }

  function initLoginPage() {
    const form = el("#ownerLoginForm");
    const passwordInput = el("#ownerPassword");
    const statusEl = el("#ownerLoginStatus");
    const submitButton = el("#ownerLoginButton");

    checkSession({
      redirectIfUnauthed: false,
      redirectIfAuthed: true
    });

    if (!form || !passwordInput || !statusEl) {
      return;
    }

    form.addEventListener("submit", async function onLoginSubmit(event) {
      event.preventDefault();
      const password = passwordInput.value.trim();

      if (!password) {
        setStatus(statusEl, "Enter your owner password to continue.", "error");
        return;
      }

      if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = "Signing in...";
      }
      setStatus(statusEl, "Checking credentials...");

      const response = await fetchJson("/api/auth/login", {
        method: "POST",
        body: { password: password }
      });

      const payload = toPayload(response.data);
      const loginSuccess = response.ok && (
        payload === null ||
        payload === undefined ||
        payload.authenticated !== false
      );

      if (loginSuccess) {
        setStatus(statusEl, "Login successful. Redirecting...", "success");
        window.location.replace("/owner/dashboard");
        return;
      }

      setStatus(
        statusEl,
        errorMessage(response.data, "Login failed. Check the password and try again."),
        "error"
      );
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.textContent = "Sign in";
      }
    });
  }

  const OwnerUI = {
    REFRESH_MS: REFRESH_MS,
    el: el,
    fetchJson: fetchJson,
    formatDate: formatDate,
    formatNumber: formatNumber,
    formatPercent: formatPercent,
    safeNumber: safeNumber,
    toPayload: toPayload,
    checkSession: checkSession,
    logout: logout,
    setStatus: setStatus
  };

  window.OwnerUI = OwnerUI;

  document.addEventListener("DOMContentLoaded", function onReady() {
    attachLogoutHandler();
    const page = document.body ? document.body.dataset.ownerPage : "";
    if (page === "login") {
      initLoginPage();
    }
  });
})();
