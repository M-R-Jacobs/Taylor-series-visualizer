# Taylor-series-visualizer
**Taylor series** (first formally published by the English mathematician Brook Taylor in 1715 and recognized by Joseph-Louis Lagrange in 1772) approximate the behavior of any function $f(x)$ as an n-th degree polynomial function, but namely help with reducing transcendental functions like: 

$$
f(x)=\sin x
$$

$$
f(x)=e^x
$$

$$
f(x)=\ln x
$$

$$
f(x)=a^x
$$

This is often useful in simplifying complex results or solving differential equations in physics and math to expressions or equations that can reduce in ways that would have been more difficult to achieve had you kept the transcendental form. For the purposes of gaining physical, real world intuition (where perfect accuracy is not necessary), Taylor approximations are critical. Applications further highlight the impact of Taylor series: making some operations in your calculator possible or easier, helping GPS recievers calculate your exact position, improving the gradient-based optimization procedures in AI LLM's; Euler's famous identity (which will be immediately recognized by physicists and engineers) also is given by this method.

$$
e^{ix}=\cos x + i~\sin x \qquad \implies \qquad e^{i\pi}=-1 \quad \text{or} \quad e^{2i\pi}=1
$$

The proof for this follows:

The starting point for the  Series is a **power series** - simply the most general infinite polynomial you could write:

$$
\sum_{n=0}^{\infty} c_n(x-a)^n = c_0 + c_1(x-a) + c_2(x-a)^2 + \cdots
$$

Each power of $(x-a)$ gets its own independent coefficient $c_n$ - there is no reason $c_0$ should equal $c_1$ or $c_2$, they are free. The question Taylor series answers is: if some function $f$ is the one producing this series, what must those coefficients actually be? As it turns out, if we know the functions derivatives, we can express it in this way.

Assume $f(x) = \sum_{n=0}^{\infty} c_n(x-a)^n$ and differentiate repeatedly, evaluating at $x = a$ each time (all terms with a factor of $(x-a)$ vanish):

$$
f(a) = c_0
$$

$$
f'(a) = c_1
$$

$$
f''(a) = 2c_2 \implies c_2 = \frac{f''(a)}{2!}
$$

$$
f^{(n)}(a) = n!~c_n \implies c_n = \frac{f^{(n)}(a)}{n!}
$$

So the derivative structures force each constant to a certain value dependant on the function's $n$-th derivative and the $n$-th factorial. Substituting back gives the Taylor series:

$$
\boxed{f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}(x-a)^n}
$$

The **Maclaurin series** is the special case $a = 0$:

$$
\boxed{f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(0)}{n!}x^n}
$$

The $n$-th degree Taylor polynomial $P_n(x)$ is just the partial sum up through degree $n$ - a finite polynomial approximation to $f$.

Since $P_n(x)$ is only a partial sum, it does not equal $f(x)$ exactly and there is some error in the approximation that grows as you move away from $a$. This is represented by the remainder function:

$$R_n(x) = f(x) - P_n(x)$$

With the generic goal of representing the Taylor series accomplished, another area of interest is to find some useful representation for $|R_n(x)|$ to evaluate it without knowing $f$ exactly - which is the whole point, since we are using $P_n$ because $f$ is hard to evaluate directly. One way which we may do this is to express $R_n$ as an integral to represent total error accumulated out to a given value of $x$, or we may simply be interested in the value of the maximum possible error. A proof of both of these follows.

*A digest on the history of the remainder polynomial:* Being that Brook Taylor's initial 1715 results were not well read (and yet were the first real publications on the subject after Gregory, Newton, and Bernoulli all put forth contributions that wasted away in unpublished manuscript collections or on the back of correspondance letters), these formulations on the remainder waited roughly 60 years until Lagrange formally addressed them in his Berlin collection of memoirs in 1772. His intent in these was to eliminate infinitesimals and fluxions from the previous century by defining derivatives as the coefficients of the Taylor expansion, and it is here where Taylor was first formally credited for the result. Lagrange's *Théorie des fonctions analytiques (1797)* would reference them as "Taylor's series" explicitly, and here is also where he formulated the error bound in the remainder polynomials. In the 2-3 decades following, Augustin-Louis Cauchy would build on this subject in integral form and attribute the error bound to Lagrange, assigning his name to the method as Lagrange did Taylor. Interestingly enough, Cauchy also demonstrated in his 1823 *Résumé des leçons sur le calcul infinitésimal* that a function can be infinitely differentiable yet fail to equal its Taylor series; this will occasionally need to be considered.

First, I would like to examine the integrated remainder result, since it will segue nicely to the error bound. Start from the Fundamental Theorem of Calculus from Leibniz:

$$f(x) = f(a) + \int_a^x f'(t)~dt$$

Integrate by parts on the integral, with $u=f'(t)$ and $v = -(x-t)$ rather than $v = t$ by taking the constant of integration to be $c=-x$ where $x$ is the upper limit of the integral; the constant of integration is free to do this. This way after evaluating at the bounds the result takes the same form as the Taylor/power series terms - powers of $(x-a)$ with factorial denominators:

$$\int_a^x f'(t)~dt = \Big[-f'(t)(x-t)\Big]_a^x + \int_a^x f''(t)(x-t)~dt = f'(a)(x-a) + \int_a^x f''(t)(x-t)~dt$$

So:

$$f(x) = f(a) + f'(a)(x-a) + \int_a^x f''(t)(x-t)~dt$$

Integrate by parts again on the new integral, choosing $v = -\dfrac{(x-t)^2}{2}$:

$$f(x) = f(a) + f'(a)(x-a) + \frac{f''(a)}{2!}(x-a)^2 + \int_a^x f'''(t)\frac{(x-t)^2}{2!}~dt$$

Each IBP step peels off one more Taylor term and bumps the power of $(x-t)$ up by one. After $n$ steps:

$$f(x) = \underbrace{\sum_{k=0}^{n}\frac{f^{(k)}(a)}{k!}(x-a)^k}_{P_n(x)} + \underbrace{\frac{1}{n!}\int_a^x f^{(n+1)}(t)(x-t)^n~dt}_{R_n(x)}$$

So the remainder has an exact integral form:

$$R_n(x) = \frac{1}{n!}\int_a^x f^{(n+1)}(t)(x-t)^n~dt$$

The integral form from Cauchy is exact, but it may not be useful - it still contains $f^{(n+1)}(t)$, which we may not be able to evaluate (the integral of). The fix is to introduce a constant ceiling for it, as is done in the work by Lagrange in 1797.

Define $M$ as the maximum value of $|f^{(n+1)}(t)|$ on the interval between $a$ and $x$:

$$M = \max_{t \in [a,~x]}\left|f^{(n+1)}(t)\right|$$

$M$ is just a number, as opposed to R, which is a function, and its size entirely reflects the behavior of $f$. A gently curving function has small higher derivatives and therefore a tight bound. A rapidly oscillating function like $\sin(10x)$ picks up a factor of $10$ with each derivative, so $f^{(n+1)}$ involves $10^{n+1}$, and $M$ is enormous - the series needs far more terms to be useful. This is the exact mechanism by which $M$ captures how well-behaved $f$ is near the approximation.

Taking absolute values of the remainder (to account for negatives), and substituting into the above expression for $R_n(x)$:

$$|R_n(x)| \leq \frac{1}{n!}\int_a^x \left|f^{(n+1)}(t)\right|(x-t)^n~dt$$

Since $|f^{(n+1)}(t)| \leq M$ for every $t$ in the interval (by definition of $M$ as the maximum), we replace it with $M$. This can only make the right side larger, so the inequality is preserved. And since $M$ is a constant with respect to $t$, it pulls cleanly outside the integral:

$$\leq \frac{M}{n!}\int_a^x (x-t)^n~dt$$

Now the integral is purely elementary (for $x>a$):

$$\int_a^x (x-t)^n~dt = \frac{(x-a)^{n+1}}{n+1}$$

Substituting:

$$|R_n(x)| \leq \frac{M}{n!}\cdot\frac{(x-a)^{n+1}}{n+1} = \frac{M}{(n+1)!}|x-a|^{n+1}$$

The entire strategy: the remainder has an exact form with an unknown function inside an integral - introduce a constant ceiling for that function, pull it out, and the remaining integral is trivial.

