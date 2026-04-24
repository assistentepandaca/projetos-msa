/**
 * A library of easing behaviours that can be used in the `easing` option of
 * animations in Remotion Animated.
 */
declare namespace Ease {
    const Linear: import("../EasingBehaviour").EasingBehaviour;
    const QuadraticIn: import("../EasingBehaviour").EasingBehaviour;
    const QuadraticOut: import("../EasingBehaviour").EasingBehaviour;
    const QuadraticInOut: import("../EasingBehaviour").EasingBehaviour;
    const CubicIn: import("../EasingBehaviour").EasingBehaviour;
    const CubicOut: import("../EasingBehaviour").EasingBehaviour;
    const CubicInOut: import("../EasingBehaviour").EasingBehaviour;
    const QuarticIn: import("../EasingBehaviour").EasingBehaviour;
    const QuarticOut: import("../EasingBehaviour").EasingBehaviour;
    const QuarticInOut: import("../EasingBehaviour").EasingBehaviour;
    const QuinticIn: import("../EasingBehaviour").EasingBehaviour;
    const QuinticOut: import("../EasingBehaviour").EasingBehaviour;
    const QuinticInOut: import("../EasingBehaviour").EasingBehaviour;
    const SinusoidalIn: import("../EasingBehaviour").EasingBehaviour;
    const SinusoidalOut: import("../EasingBehaviour").EasingBehaviour;
    const SinusoidalInOut: import("../EasingBehaviour").EasingBehaviour;
    const CircularIn: import("../EasingBehaviour").EasingBehaviour;
    const CircularOut: import("../EasingBehaviour").EasingBehaviour;
    const CircularInOut: import("../EasingBehaviour").EasingBehaviour;
    const ExponentialIn: import("../EasingBehaviour").EasingBehaviour;
    const ExponentialOut: import("../EasingBehaviour").EasingBehaviour;
    const ExponentialInOut: import("../EasingBehaviour").EasingBehaviour;
    const BounceIn: import("../EasingBehaviour").EasingBehaviour;
    const BounceOut: import("../EasingBehaviour").EasingBehaviour;
    const BounceInOut: import("../EasingBehaviour").EasingBehaviour;
    /**
     * Defines a custom cubic bezier curve.
     */
    const Bezier: (x1: number, y1: number, x2: number, y2: number) => import("../EasingBehaviour").EasingBehaviour;
}
export default Ease;
//# sourceMappingURL=Ease.d.ts.map