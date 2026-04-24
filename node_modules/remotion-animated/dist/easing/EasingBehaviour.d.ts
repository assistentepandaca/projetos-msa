import AnimationOptions from '../animations/AnimationOptions';
/**
 * An easing behaviour is a function that takes in the current frame, the FPS,
 * and options and returns a driver value.
 *
 * You'll typically use easing behaviours from the `Ease` namespace from
 * `remotion-animated`, such as `Ease.Linear`, `Ease.Cubic`, etc.,
 * or you can create a custom easing behaviour using the `CustomEasing` function.
 */
export type EasingBehaviour = (frame: number, fps: number, options: AnimationOptions) => {
    driver: number;
};
export declare const easingForOptions: (options: AnimationOptions, defaultingTo?: EasingBehaviour) => EasingBehaviour;
export declare const valueWithEasing: (frame: number, fps: number, options: AnimationOptions, defaultingTo?: EasingBehaviour) => number;
//# sourceMappingURL=EasingBehaviour.d.ts.map