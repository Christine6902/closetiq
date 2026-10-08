// Vanilla-JS calculator. No inline handlers, no eval — a small state machine
// drives an accumulator so chained operations (e.g. 2 + 3 × 4 =) behave the
// way a physical calculator does.
(function () {
    "use strict";

    var MAX_DIGITS = 12;

    var state = {
        current: "0",     // string being entered / shown
        stored: null,     // previous operand (number)
        operator: null,   // pending operator: + - * /
        overwrite: true   // next digit replaces the display
    };

    var resultEl, expressionEl, keysEl;

    var OPERATOR_SYMBOL = { "+": "+", "-": "−", "*": "×", "/": "÷" };

    function compute(a, b, op) {
        switch (op) {
            case "+": return a + b;
            case "-": return a - b;
            case "*": return a * b;
            case "/": return b === 0 ? NaN : a / b;
            default:  return b;
        }
    }

    // Format a number for the display: trim float noise, cap length, keep it readable.
    function format(n) {
        if (!isFinite(n)) return "Error";
        if (n === 0) return "0";

        var rounded = parseFloat(n.toPrecision(MAX_DIGITS));
        var str = String(rounded);

        if (str.replace(/[-.]/g, "").length > MAX_DIGITS || Math.abs(rounded) >= 1e12) {
            str = rounded.toExponential(6).replace(/\.?0+e/, "e");
        }
        return str;
    }

    function render() {
        resultEl.textContent = state.current;

        var expr = "";
        if (state.stored !== null && state.operator) {
            expr = format(state.stored) + " " + OPERATOR_SYMBOL[state.operator];
        }
        expressionEl.innerHTML = expr === "" ? "&nbsp;" : expr;

        // Highlight the pending operator key.
        var pending = state.overwrite && state.operator !== null && state.stored !== null;
        var keys = keysEl.querySelectorAll("[data-operator]");
        for (var i = 0; i < keys.length; i++) {
            var active = pending && keys[i].getAttribute("data-operator") === state.operator;
            keys[i].classList.toggle("is-active", active);
        }
    }

    function inputDigit(d) {
        if (resultEl.textContent === "Error") clearAll();
        if (state.overwrite) {
            state.current = d === "0" ? "0" : d;
            state.overwrite = false;
        } else if (state.current === "0") {
            state.current = d === "0" ? "0" : d;
        } else if (state.current.replace(/[-.]/g, "").length < MAX_DIGITS) {
            state.current += d;
        }
        render();
    }

    function inputDecimal() {
        if (resultEl.textContent === "Error") clearAll();
        if (state.overwrite) {
            state.current = "0.";
            state.overwrite = false;
        } else if (state.current.indexOf(".") === -1) {
            state.current += ".";
        }
        render();
    }

    function toggleSign() {
        if (state.current === "0" || state.current === "Error") return;
        state.current = state.current.charAt(0) === "-"
            ? state.current.slice(1)
            : "-" + state.current;
        render();
    }

    function percent() {
        var value = parseFloat(state.current);
        if (isNaN(value)) return;
        state.current = format(value / 100);
        state.overwrite = true;
        render();
    }

    function chooseOperator(op) {
        var entered = parseFloat(state.current);

        if (state.operator && !state.overwrite && state.stored !== null) {
            // Chain: fold the pending op before applying the new one.
            var folded = compute(state.stored, entered, state.operator);
            state.stored = folded;
            state.current = format(folded);
        } else if (state.stored === null) {
            state.stored = entered;
        }

        state.operator = op;
        state.overwrite = true;
        render();
    }

    function equals() {
        if (state.operator === null || state.stored === null) return;
        var entered = parseFloat(state.current);
        var result = compute(state.stored, entered, state.operator);

        state.current = format(result);
        state.stored = null;
        state.operator = null;
        state.overwrite = true;
        render();
    }

    function clearAll() {
        state.current = "0";
        state.stored = null;
        state.operator = null;
        state.overwrite = true;
        render();
    }

    function handleKeyEl(el) {
        if (el.hasAttribute("data-digit"))    { inputDigit(el.getAttribute("data-digit")); return; }
        if (el.hasAttribute("data-operator")) { chooseOperator(el.getAttribute("data-operator")); return; }
        switch (el.getAttribute("data-action")) {
            case "decimal": inputDecimal(); break;
            case "sign":    toggleSign();   break;
            case "percent": percent();      break;
            case "equals":  equals();       break;
            case "clear":   clearAll();     break;
        }
    }

    function handleKeyboard(e) {
        var k = e.key;
        if (k >= "0" && k <= "9")            { inputDigit(k); e.preventDefault(); }
        else if (k === ".")                  { inputDecimal(); }
        else if (k === "+" || k === "-" || k === "*" || k === "/") { chooseOperator(k); }
        else if (k === "Enter" || k === "=") { equals(); e.preventDefault(); }
        else if (k === "%")                  { percent(); }
        else if (k === "Escape")             { clearAll(); }
        else if (k === "Backspace") {
            if (!state.overwrite) {
                state.current = state.current.length > 1 ? state.current.slice(0, -1) : "0";
                if (state.current === "-") state.current = "0";
                if (state.current === "0") state.overwrite = true;
                render();
            }
        }
    }

    function init() {
        resultEl = document.getElementById("calc-result");
        expressionEl = document.getElementById("calc-expression");
        keysEl = document.querySelector(".calc-keys");
        if (!resultEl || !keysEl) return;

        keysEl.addEventListener("click", function (e) {
            var btn = e.target.closest(".calc-key");
            if (btn) handleKeyEl(btn);
        });
        document.addEventListener("keydown", handleKeyboard);

        clearAll();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
