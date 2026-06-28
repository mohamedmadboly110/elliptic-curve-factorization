# Elliptic Curve Factorization Engine (Lenstra's ECM)

A lightweight, educational, and pure Python implementation of **Lenstra's Elliptic Curve Method (ECM)** for integer factorization. This project simulates the collapse of elliptic curve groups over composite moduli to extract non-trivial prime factors, mimicking advanced cryptographic cryptanalysis tools without relying on heavy external dependencies.

## 📌 Project Overview
Integer factorization is the foundational bottleneck behind the security of public-key cryptography systems like RSA. While trial division and standard algorithms struggle with large numbers, Lenstra's ECM utilizes the geometric properties of algebraic curves to find factors in sub-exponential time. 

This engine is optimized for academic presentation, employing standard **Affine Coordinates** ($x, y$) for clear mathematical readability and absolute structural transparency.

---

## 🚀 Key Features

* **Pure Python Architecture:** Runs natively on standard Python installations without requiring external C-libraries (`gmpy2`, `primesieve`, etc.).
* **Pre-computation Optimization Layers:** 
  1. **Primality Pre-check:** Automatically filters out prime inputs to prevent unnecessary CPU looping.
  2. **Perfect Power Detector (`is_perfect_power`):** Identifies edge-case integers ($x^2, x^3$) that inherently cause geometric factorization failures, handling them instantly.
* **Standard Affine Geometry:** Implements explicit Point Addition and Point Doubling formulas from scratch, making it an excellent resource for thesis and project documentation.
* **The Modular Inverse Trap:** Captures the exact algebraic step where the Extended Euclidean Algorithm fails, extracting the prime factor via the Greatest Common Divisor (GCD).

---

## 🧬 How It Works (The Core Mechanism)

The engine sets up a random elliptic curve mapped over the target composite number $n$:

$$y^2 = x^3 + ax + b \pmod n$$

1. It selects a random starting point $P(x_1, y_1)$ on the curve.
2. It attempts scalar multiplication ($k \cdot P$) by continuously calculating the geometric slope ($\lambda$).
3. To compute $\lambda$, a modular inverse of the denominator is required:
   $$\lambda = \frac{y_2 - y_1}{x_2 - x_1} \pmod n$$
4. If $n$ is composite, the arithmetic eventually hits a point where the denominator shares a factor with $n$. The modular inverse fails, and the algorithm traps that denominator to compute $\gcd(\text{denominator}, n)$, revealing the hidden prime factor!

---

## 💻 Usage

Simply clone or download the file and run it inside your terminal:

```bash
python elliptic_factor.py
