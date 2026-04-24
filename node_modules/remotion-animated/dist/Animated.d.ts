import React from 'react';
import Animation from './animations/Animation';
export interface AnimatedProps {
    /** List of all [animations](https://www.remotion-animated.dev/docs/category/animations) for this element. (The order is relevant if there are multiple animations that affect the same property.) */
    animations: Animation[];
    /** If true, the animation container will be positioned absolutely. _Defaults to `false`._ */
    absolute?: boolean;
    /** Frame number at which the animation container starts being visible ("In" point), if set. */
    in?: number;
    /** Frame number after which the animation container stops being visible ("Out" point), if set. */
    out?: number;
    /** Number of frames by which all animation starts are delayed. Does not affect in and out. _Defaults to `0`._ */
    delay?: number;
    /** Class name that is applied to the animation container. */
    className?: string;
    /** Children that are rendered inside the animation container. */
    children?: React.ReactNode;
    /** Styles that are applied to the animation container. */
    style?: React.CSSProperties;
}
/**
 * The `Animated` component renders a container that can be animated.
 */
declare const Animated: (props: AnimatedProps) => import("react/jsx-runtime").JSX.Element | null;
export default Animated;
//# sourceMappingURL=Animated.d.ts.map