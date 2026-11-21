/**
 * Smart Calculator - PWA Controller and UI Manager
 * Handles user interactions, PWA lifecycle, localStorage history, themes, and keyboard bindings.
 */

class CalculatorApp {
  constructor() {
    this.expression = "";
    this.result = "0";
    this.justEvaluated = false;
    this.isScientific = false;
    this.history = this.loadHistory();
    this.deferredPrompt = null;

    this.cacheDOMElements();
    this.initPWA();
    this.initTheme();
    this.bindEvents();
    this.renderDisplay();
    this.renderHistory();

    // Dismiss loading splash screen
    setTimeout(() => {
      const splash = document.getElementById("loading-screen");
      if (splash) splash.classList.add("hidden");
    }, 350);
  }

  cacheDOMElements() {
    this.appContainer = document.getElementById("calculator-app");
    this.expressionEl = document.getElementById("expression-display");
    this.resultEl = document.getElementById("result-display");
    this.modeBtn = document.getElementById("mode-toggle-btn");
    this.modeBadge = document.getElementById("mode-badge");
    this.themeBtn = document.getElementById("theme-toggle-btn");
    this.historyBtn = document.getElementById("history-toggle-btn");
    this.installBtn = document.getElementById("install-pwa-btn");
    this.historyDrawer = document.getElementById("history-drawer");
    this.closeHistoryBtn = document.getElementById("close-history-btn");
    this.historyListEl = document.getElementById("history-list");
    this.clearHistoryBtn = document.getElementById("clear-history-btn");
    this.keypad = document.getElementById("keypad");
  }

  // ------------------ PWA Registration & Install Prompt ------------------

  initPWA() {
    // 1. Register Service Worker for offline capability
    if ("serviceWorker" in navigator) {
      window.addEventListener("load", () => {
        navigator.serviceWorker
          .register("./sw.js")
          .then((reg) => {
            console.log("[PWA] Service Worker registered with scope:", reg.scope);
          })
          .catch((err) => {
            console.warn("[PWA] Service Worker registration failed:", err);
          });
      });
    }

    // 2. Capture 'beforeinstallprompt' to enable custom Install button
    window.addEventListener("beforeinstallprompt", (e) => {
      e.preventDefault();
      this.deferredPrompt = e;
      if (this.installBtn) {
        this.installBtn.classList.add("visible");
      }
    });

    window.addEventListener("appinstalled", () => {
      console.log("[PWA] Smart Calculator was installed successfully.");
      if (this.installBtn) {
        this.installBtn.classList.remove("visible");
      }
      this.deferredPrompt = null;
    });
  }

  triggerInstall() {
    if (!this.deferredPrompt) {
      alert("To install this app on your device:\n\n• On Chrome / Edge (Desktop): Click the install icon in the browser address bar.\n• On Android (Chrome): Tap browser menu (⋮) -> 'Add to Home screen' or 'Install app'.\n• On iPhone / iPad (Safari): Tap the Share button (⎋) -> 'Add to Home Screen'.");
      return;
    }
    this.deferredPrompt.prompt();
    this.deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === "accepted") {
        console.log("[PWA] User accepted the installation");
      }
      this.deferredPrompt = null;
      this.installBtn.classList.remove("visible");
    });
  }

  // ------------------ Theme Management ------------------

  initTheme() {
    const savedTheme = localStorage.getItem("smart_calc_theme") || "dark";
    this.setTheme(savedTheme);
  }

  setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("smart_calc_theme", theme);
    if (this.themeBtn) {
      this.themeBtn.innerHTML = theme === "dark" ? "☀️ Light" : "🌙 Dark";
    }

    // Update meta theme-color for browser tab / mobile status bar
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
      metaThemeColor.setAttribute("content", theme === "dark" ? "#18181b" : "#4f46e5");
    }
  }

  toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme") || "dark";
    const next = current === "dark" ? "light" : "dark";
    this.setTheme(next);
  }

  // ------------------ Event Listeners ------------------

  bindEvents() {
    // Mode toggle
    this.modeBtn.addEventListener("click", () => this.toggleScientificMode());

    // Theme toggle
    this.themeBtn.addEventListener("click", () => this.toggleTheme());

    // History toggle
    this.historyBtn.addEventListener("click", () => this.toggleHistoryDrawer());
    this.closeHistoryBtn.addEventListener("click", () => this.toggleHistoryDrawer(false));
    this.clearHistoryBtn.addEventListener("click", () => this.clearAllHistory());

    // Install PWA
    if (this.installBtn) {
      this.installBtn.addEventListener("click", () => this.triggerInstall());
    }

    // Keypad clicks (delegated)
    this.keypad.addEventListener("click", (e) => {
      const btn = e.target.closest(".calc-btn");
      if (!btn) return;

      this.triggerHapticFeedback();
      const action = btn.dataset.action;
      const value = btn.dataset.value;

      this.handleInput(action, value);
    });

    // Keyboard support
    window.addEventListener("keydown", (e) => this.handleKeyboard(e));
  }

  triggerHapticFeedback() {
    if ("vibrate" in navigator) {
      try {
        navigator.vibrate(10);
      } catch (err) {
        // Ignored on unsupported devices
      }
    }
  }

  // ------------------ Calculator Input Handler ------------------

  handleInput(action, value) {
    switch (action) {
      case "number":
        this.inputNumber(value);
        break;
      case "operator":
        this.inputOperator(value);
        break;
      case "function":
        this.inputFunction(value);
        break;
      case "constant":
        this.inputConstant(value);
        break;
      case "bracket":
        this.inputBracket(value);
        break;
      case "equal":
        this.calculate();
        break;
      case "clear":
        this.clearAll();
        break;
      case "delete":
        this.deleteChar();
        break;
      case "toggle-sign":
        this.toggleSign();
        break;
      case "percentage":
        this.inputPercentage();
        break;
      case "reciprocal":
        this.inputReciprocal();
        break;
      case "square":
        this.inputSquare();
        break;
      case "factorial":
        this.inputFactorial();
        break;
    }
  }

  inputNumber(num) {
    if (this.justEvaluated) {
      this.expression = "";
      this.justEvaluated = false;
    }

    if (num === "." && this.expression.endsWith(".")) return;
    this.expression += num;
    this.renderDisplay();
  }

  inputOperator(op) {
    if (this.justEvaluated) {
      this.justEvaluated = false;
    }

    if (!this.expression) {
      if (op === "−") {
        this.expression = "-";
        this.renderDisplay();
      } else if (this.result !== "0" && this.result !== "Error") {
        this.expression = `${this.result} ${op} `;
        this.renderDisplay();
      }
      return;
    }

    const trimmed = this.expression.trimEnd();
    const lastChar = trimmed[trimmed.length - 1];
    if (["+", "−", "×", "÷", "^", "-"].includes(lastChar)) {
      this.expression = trimmed.slice(0, -1) + op + " ";
    } else {
      this.expression += ` ${op} `;
    }

    this.renderDisplay();
  }

  inputFunction(funcName) {
    if (this.justEvaluated) {
      this.expression = "";
      this.justEvaluated = false;
    }
    this.expression += `${funcName}(`;
    this.renderDisplay();
  }

  inputConstant(constName) {
    if (this.justEvaluated) {
      this.expression = "";
      this.justEvaluated = false;
    }
    this.expression += constName === "pi" ? "π" : constName;
    this.renderDisplay();
  }

  inputBracket(paren) {
    if (this.justEvaluated) {
      this.justEvaluated = false;
    }
    this.expression += paren;
    this.renderDisplay();
  }

  inputPercentage() {
    if (this.justEvaluated) {
      this.justEvaluated = false;
    }
    this.expression += "%";
    this.renderDisplay();
  }

  inputReciprocal() {
    if (!this.expression && this.result !== "0" && this.result !== "Error") {
      this.expression = `1/(${this.result})`;
    } else {
      this.expression = `1/(${this.expression || ""}`;
    }
    this.justEvaluated = false;
    this.renderDisplay();
  }

  inputSquare() {
    if (!this.expression && this.result !== "0" && this.result !== "Error") {
      this.expression = `(${this.result})^2`;
    } else {
      this.expression += "^2";
    }
    this.justEvaluated = false;
    this.renderDisplay();
  }

  inputFactorial() {
    if (!this.expression && this.result !== "0" && this.result !== "Error") {
      this.expression = `fact(${this.result})`;
    } else {
      this.expression = `fact(${this.expression}`;
    }
    this.justEvaluated = false;
    this.renderDisplay();
  }

  toggleSign() {
    if (!this.expression) {
      this.expression = "-";
    } else if (this.expression.startsWith("-(")) {
      this.expression = this.expression.slice(2, -1);
    } else if (this.expression.startsWith("-")) {
      this.expression = this.expression.slice(1);
    } else {
      this.expression = `-(${this.expression})`;
    }
    this.renderDisplay();
  }

  clearAll() {
    this.expression = "";
    this.result = "0";
    this.justEvaluated = false;
    this.renderDisplay();
  }

  deleteChar() {
    if (this.justEvaluated) {
      this.justEvaluated = false;
    }

    if (this.expression) {
      if (this.expression.endsWith(" ")) {
        this.expression = this.expression.trimEnd();
      } else {
        this.expression = this.expression.slice(0, -1);
      }
    }
    this.renderDisplay();
  }

  calculate() {
    if (!this.expression.trim()) return;

    const rawExpr = this.expression.trim();

    try {
      const computedValue = SafeExpressionEvaluator.evaluate(rawExpr);
      const formatted = SmartCalculator.formatResult(computedValue);

      this.result = formatted;
      this.saveHistory(rawExpr, formatted);

      this.expressionEl.textContent = `${rawExpr} =`;
      this.resultEl.textContent = formatted;
      this.resultEl.classList.remove("error");

      this.expression = formatted;
      this.justEvaluated = true;
    } catch (err) {
      this.expressionEl.textContent = `${rawExpr} =`;
      this.resultEl.textContent = err.message || "Invalid Input";
      this.resultEl.classList.add("error");
      this.justEvaluated = true;
    }
  }

  renderDisplay() {
    this.expressionEl.textContent = this.expression;
    this.resultEl.textContent = this.expression ? this.expression : "0";
    this.resultEl.classList.remove("error");

    // Auto-scroll display to the right end
    this.expressionEl.scrollLeft = this.expressionEl.scrollWidth;
    this.resultEl.scrollLeft = this.resultEl.scrollWidth;
  }

  // ------------------ Mode Toggle ------------------

  toggleScientificMode() {
    this.isScientific = !this.isScientific;

    if (this.isScientific) {
      this.appContainer.classList.add("scientific-active");
      this.modeBtn.textContent = "Standard";
      this.modeBtn.classList.add("active");
      this.modeBadge.textContent = "Scientific";
    } else {
      this.appContainer.classList.remove("scientific-active");
      this.modeBtn.textContent = "Scientific";
      this.modeBtn.classList.remove("active");
      this.modeBadge.textContent = "Standard";
    }
  }

  // ------------------ History Drawer & LocalStorage ------------------

  loadHistory() {
    try {
      const stored = localStorage.getItem("smart_calc_history");
      return stored ? JSON.parse(stored) : [];
    } catch (e) {
      return [];
    }
  }

  saveHistory(expr, res) {
    const record = {
      id: Date.now(),
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      expression: expr,
      result: res,
    };
    this.history.unshift(record);
    if (this.history.length > 50) this.history.pop();

    localStorage.setItem("smart_calc_history", JSON.stringify(this.history));
    this.renderHistory();
  }

  deleteHistoryItem(id, event) {
    if (event) event.stopPropagation();
    this.history = this.history.filter((item) => item.id !== id);
    localStorage.setItem("smart_calc_history", JSON.stringify(this.history));
    this.renderHistory();
  }

  clearAllHistory() {
    if (confirm("Clear all calculation history?")) {
      this.history = [];
      localStorage.removeItem("smart_calc_history");
      this.renderHistory();
    }
  }

  reuseHistoryResult(resultValue) {
    this.expression = resultValue.toString();
    this.result = resultValue.toString();
    this.justEvaluated = false;
    this.renderDisplay();
    this.toggleHistoryDrawer(false);
  }

  toggleHistoryDrawer(open = null) {
    const shouldOpen = open !== null ? open : !this.historyDrawer.classList.contains("open");
    if (shouldOpen) {
      this.historyDrawer.classList.add("open");
      this.historyBtn.classList.add("active");
    } else {
      this.historyDrawer.classList.remove("open");
      this.historyBtn.classList.remove("active");
    }
  }

  renderHistory() {
    if (!this.historyListEl) return;
    this.historyListEl.innerHTML = "";

    if (this.history.length === 0) {
      this.historyListEl.innerHTML = '<div class="history-empty">No calculations yet.<br>Perform operations to see them here.</div>';
      return;
    }

    this.history.forEach((item) => {
      const itemEl = document.createElement("div");
      itemEl.className = "history-item";
      itemEl.innerHTML = `
        <div class="history-content">
          <div class="history-expr">${item.expression}</div>
          <div class="history-res">= ${item.result}</div>
          <div class="history-time">${item.timestamp}</div>
        </div>
        <button class="item-delete-btn" title="Delete entry" aria-label="Delete entry">🗑</button>
      `;

      itemEl.addEventListener("click", () => this.reuseHistoryResult(item.result));

      const delBtn = itemEl.querySelector(".item-delete-btn");
      delBtn.addEventListener("click", (e) => this.deleteHistoryItem(item.id, e));

      this.historyListEl.appendChild(itemEl);
    });
  }

  // ------------------ Desktop Keyboard Support ------------------

  handleKeyboard(e) {
    const key = e.key;

    if (/^[0-9.]$/.test(key)) {
      this.inputNumber(key);
    } else if (key === "+") {
      this.inputOperator("+");
    } else if (key === "-") {
      this.inputOperator("−");
    } else if (key === "*") {
      this.inputOperator("×");
    } else if (key === "/") {
      e.preventDefault();
      this.inputOperator("÷");
    } else if (key === "^") {
      this.inputOperator("^");
    } else if (key === "%") {
      this.inputPercentage();
    } else if (key === "(" || key === ")") {
      this.inputBracket(key);
    } else if (key === "Enter" || key === "=") {
      e.preventDefault();
      this.calculate();
    } else if (key === "Backspace") {
      this.deleteChar();
    } else if (key === "Escape" || key.toLowerCase() === "c") {
      this.clearAll();
    } else if (key.toLowerCase() === "s") {
      this.inputFunction("sin");
    } else if (key.toLowerCase() === "o") {
      this.inputFunction("cos");
    } else if (key.toLowerCase() === "t") {
      this.inputFunction("tan");
    } else if (key.toLowerCase() === "l") {
      this.inputFunction("log");
    } else if (key.toLowerCase() === "p") {
      this.inputConstant("pi");
    }
  }
}

// Instantiate on DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  window.smartCalcApp = new CalculatorApp();
});
