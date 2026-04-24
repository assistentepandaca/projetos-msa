import Animation from './Animation';
import AnimationOptions from './AnimationOptions';
export type MoveOptions = AnimationOptions & {
    /** The element will be moved to the right by this amount (in pixels). */
    x?: number;
    /** The element will be moved down by this amount (in pixels). */
    y?: number;
    /** The element will be moved along the z-axis by this amount (in pixels). */
    z?: number;
    /** The x position offset that is used at the start of the animation (in pixels). _Defaults to `0`._ */
    initialX?: number;
    /** The y position offset that is used at the start of the animation (in pixels). Defaults to `0`. */
    initialY?: number;
    /** The z position offset that is used at the start of the animation (in pixels). Defaults to `0`. */
    initialZ?: number;
};
/**
 * The `Move` animation translates an element horizontally, vertically or both.
 */
declare const Move: (options: MoveOptions) => Animation;
export default Move;
//# sourceMappingURL=Move.d.ts.map