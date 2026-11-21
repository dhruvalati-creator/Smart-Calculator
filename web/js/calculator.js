/**
 * Smart Calculator - Core Mathematical Engine
 * Replicates the complete Python SmartCalculator and SafeExpressionEvaluator logic.
 */

class SmartCalculator {
  // ------------------ Basic Operations ------------------

  static add(a, b) {
    return a + b;
  }

  static subtract(a, b) {
    return a - b;
  }

  static multiply(a, b) {
    return a * b;
  }

  static divide(a, b) {
    if (b === 0) {
      throw new Error("Division by zero is not allowed.");
    }
    return a / b;
  }

  // ------------------ Percentage Operations ------------------

  static percentage(total, percent) {
    return (percent / 100.0) * total;
  }

  static percentageOf(part, whole) {
    if (whole === 0) {
      throw new Error("Cannot calculate percentage of whole = 0.");
    }
    return (part / whole) * 100.0;
  }

  // ------------------ Power & Root Operations ------------------

  static power(base, exponent) {
    return Math.pow(base, exponent);
  }

  static square(x) {
    return x * x;
  }

  static squareRoot(x) {
    if (x < 0) {
      throw new Error("Cannot calculate square root of a negative number in real numbers.");
    }
    return Math.sqrt(x);
  }

  static reciprocal(x) {
    if (x === 0) {
      throw new Error("Cannot divide by zero for reciprocal (1/0).");
    }
    return 1.0 / x;
  }

  // ------------------ Scientific Operations ------------------

  static sin(degrees) {
    const normalized = degrees % 360;
    if (normalized === 0 || Math.abs(normalized) === 180 || Math.abs(normalized) === 360) {
      return 0;
    }
    const radians = (degrees * Math.PI) / 180.0;
    const res = Math.sin(radians);
    return Math.round(res * 1e10) / 1e10;
  }

  static cos(degrees) {
    const normalized = Math.abs(degrees % 360);
    if (normalized === 90 || normalized === 270) {
      return 0;
    }
    const radians = (degrees * Math.PI) / 180.0;
    const res = Math.cos(radians);
    return Math.round(res * 1e10) / 1e10;
  }

  static tan(degrees) {
    const normalized = Math.abs(degrees % 180);
    if (Math.abs(normalized - 90) < 1e-7) {
      throw new Error(`tan(${degrees}°) is undefined (asymptote).`);
    }
    const radians = (degrees * Math.PI) / 180.0;
    const res = Math.tan(radians);
    return Math.round(res * 1e10) / 1e10;
  }

  static log10(x) {
    if (x <= 0) {
      throw new Error("Logarithm is only defined for numbers greater than 0.");
    }
    return Math.log10(x);
  }

  static ln(x) {
    if (x <= 0) {
      throw new Error("Natural logarithm is only defined for numbers greater than 0.");
    }
    return Math.log(x);
  }

  static factorial(n) {
    if (!Number.isInteger(n) || n < 0) {
      throw new Error("Factorial is only defined for non-negative integers.");
    }
    if (n > 170) {
      throw new Error("Result too large (overflow).");
    }
    let res = 1;
    for (let i = 2; i <= n; i++) {
      res *= i;
    }
    return res;
  }

  // ------------------ Helper Formatting ------------------

  static formatResult(value) {
    if (typeof value !== "number" || isNaN(value)) {
      return "Error";
    }
    if (!isFinite(value)) {
      return value > 0 ? "Infinity" : "-Infinity";
    }
    // Clean precision artifacts like 0.1 + 0.2 = 0.30000000000000004
    const rounded = parseFloat(value.toPrecision(12));
    if (Number.isInteger(rounded)) {
      return rounded.toString();
    }
    // Limit decimal display cleanly
    const str = rounded.toString();
    if (str.includes("e")) {
      return rounded.toExponential(4);
    }
    return str;
  }
}

/**
 * Safe Mathematical Expression Evaluator
 * Uses a recursive descent parser with operator precedence.
 * Completely eliminates any use of JavaScript eval() or Function().
 */
class SafeExpressionEvaluator {
  static sanitize(expr) {
    if (!expr) return "";
    let s = expr.trim();

    // Standardize unicode symbols
    s = s.replace(/×/g, "*").replace(/÷/g, "/").replace(/−/g, "-").replace(/–/g, "-");
    s = s.replace(/π/g, "pi");
    s = s.replace(/\^/g, "**");

    // Replace square root symbols
    s = s.replace(/√\s*(\d+(?:\.\d+)?)/g, "sqrt($1)");
    s = s.replace(/√\s*\(/g, "sqrt(");

    // Percentage conversion: e.g. 50% -> (50*0.01)
    s = s.replace(/(\d+(?:\.\d+)?)\s*%/g, "($1*0.01)");

    // Implicit multiplication:
    // Number followed by parenthesis: 2( -> 2*(
    s = s.replace(/(\d)\s*\(/g, "$1*(");
    // ) followed by (: )( -> )*(
    s = s.replace(/\)\s*\(/g, ")*(");
    // ) followed by number: )2 -> )*2
    s = s.replace(/\)\s*(\d)/g, ")*$1");
    // Number followed by letter: 5sin -> 5*sin, 5pi -> 5*pi
    s = s.replace(/(\d)\s*([a-zA-Z])/g, "$1*$2");
    // ) followed by letter: )sin -> )*sin
    s = s.replace(/\)\s*([a-zA-Z])/g, ")*$2");

    // Balance open parentheses
    const openParen = (s.match(/\(/g) || []).length;
    const closeParen = (s.match(/\)/g) || []).length;
    if (openParen > closeParen) {
      s += ")".repeat(openParen - closeParen);
    }

    return s;
  }

  static tokenize(expr) {
    const tokens = [];
    let i = 0;
    while (i < expr.length) {
      const c = expr[i];

      if (/\s/.test(c)) {
        i++;
        continue;
      }

      // Numbers (integers or decimals)
      if (/\d/.test(c) || (c === "." && i + 1 < expr.length && /\d/.test(expr[i + 1]))) {
        let numStr = "";
        while (i < expr.length && (/\d/.test(expr[i]) || expr[i] === ".")) {
          numStr += expr[i];
          i++;
        }
        tokens.push({ type: "NUMBER", value: parseFloat(numStr) });
        continue;
      }

      // Identifiers / Function names / Constants
      if (/[a-zA-Z]/.test(c)) {
        let ident = "";
        while (i < expr.length && /[a-zA-Z0-9]/.test(expr[i])) {
          ident += expr[i];
          i++;
        }
        tokens.push({ type: "IDENT", value: ident.toLowerCase() });
        continue;
      }

      // Exponentiation operator **
      if (c === "*" && i + 1 < expr.length && expr[i + 1] === "*") {
        tokens.push({ type: "OP", value: "**" });
        i += 2;
        continue;
      }

      // Single character operators & parentheses
      if ("+-*/()%,^".includes(c)) {
        tokens.push({ type: c === "(" || c === ")" ? "PAREN" : "OP", value: c });
        i++;
        continue;
      }

      throw new Error(`Unexpected character: '${c}'`);
    }
    return tokens;
  }

  static evaluate(exprString) {
    const sanitized = this.sanitize(exprString);
    if (!sanitized) {
      throw new Error("Expression is empty.");
    }

    const tokens = this.tokenize(sanitized);
    let index = 0;

    function peek() {
      return tokens[index];
    }

    function consume(expectedValue) {
      const token = tokens[index];
      if (!token || (expectedValue && token.value !== expectedValue)) {
        throw new Error(`Expected '${expectedValue}' but got '${token ? token.value : "EOF"}'`);
      }
      index++;
      return token;
    }

    // Grammar Hierarchy:
    // parseExpression -> parseAddSub
    // parseAddSub -> parseMulDivMod
    // parseMulDivMod -> parsePower
    // parsePower -> parseUnary
    // parseUnary -> parsePrimary
    // parsePrimary -> Number | Constant | FunctionCall | (Expression)

    function parseExpression() {
      return parseAddSub();
    }

    function parseAddSub() {
      let left = parseMulDivMod();
      while (peek() && (peek().value === "+" || peek().value === "-")) {
        const op = consume().value;
        const right = parseMulDivMod();
        if (op === "+") {
          left = SmartCalculator.add(left, right);
        } else {
          left = SmartCalculator.subtract(left, right);
        }
      }
      return left;
    }

    function parseMulDivMod() {
      let left = parsePower();
      while (peek() && (peek().value === "*" || peek().value === "/" || peek().value === "%")) {
        const op = consume().value;
        const right = parsePower();
        if (op === "*") {
          left = SmartCalculator.multiply(left, right);
        } else if (op === "/") {
          left = SmartCalculator.divide(left, right);
        } else if (op === "%") {
          if (right === 0) throw new Error("Modulo by zero is not allowed.");
          left = left % right;
        }
      }
      return left;
    }

    function parsePower() {
      let left = parseUnary();
      if (peek() && (peek().value === "**" || peek().value === "^")) {
        consume();
        const right = parsePower(); // right-associative
        left = SmartCalculator.power(left, right);
      }
      return left;
    }

    function parseUnary() {
      if (peek() && (peek().value === "+" || peek().value === "-")) {
        const op = consume().value;
        const operand = parseUnary();
        return op === "-" ? -operand : +operand;
      }
      return parsePrimary();
    }

    function parsePrimary() {
      const token = peek();
      if (!token) {
        throw new Error("Unexpected end of expression.");
      }

      if (token.type === "NUMBER") {
        consume();
        return token.value;
      }

      if (token.type === "IDENT") {
        const name = token.value;
        consume();

        // Constants
        if (name === "pi") return Math.PI;
        if (name === "e") return Math.E;

        // Function Calls
        if (peek() && peek().value === "(") {
          consume("(");
          const arg = parseExpression();
          consume(")");

          switch (name) {
            case "sin":
              return SmartCalculator.sin(arg);
            case "cos":
              return SmartCalculator.cos(arg);
            case "tan":
              return SmartCalculator.tan(arg);
            case "sqrt":
              return SmartCalculator.squareRoot(arg);
            case "log":
            case "log10":
              return SmartCalculator.log10(arg);
            case "ln":
              return SmartCalculator.ln(arg);
            case "fact":
            case "factorial":
              return SmartCalculator.factorial(arg);
            case "sqr":
              return SmartCalculator.square(arg);
            case "recip":
            case "reciprocal":
              return SmartCalculator.reciprocal(arg);
            default:
              throw new Error(`Unknown function: '${name}'`);
          }
        }

        throw new Error(`Unknown identifier: '${name}'`);
      }

      if (token.value === "(") {
        consume("(");
        const val = parseExpression();
        consume(")");
        return val;
      }

      throw new Error(`Unexpected token: '${token.value}'`);
    }

    const result = parseExpression();
    if (index < tokens.length) {
      throw new Error(`Unexpected token at end: '${tokens[index].value}'`);
    }

    return result;
  }
}

// Export for Node/CommonJS (if testing) and browser window
if (typeof module !== "undefined" && module.exports) {
  module.exports = { SmartCalculator, SafeExpressionEvaluator };
} else if (typeof window !== "undefined") {
  window.SmartCalculator = SmartCalculator;
  window.SafeExpressionEvaluator = SafeExpressionEvaluator;
}
