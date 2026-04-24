import Animation from './Animation';
import AnimationOptions from './AnimationOptions';
export type SizeOptions = AnimationOptions & {
    /** The element's width will be animated to this value, if set. */
    width?: number;
    /** The element's height will be animated to this value, if set. */
    height?: number;
    /** The width that is used at the start of the animation. Defaults to `0`. */
    initialWidth?: number;
    /** The height that is used at the start of the animation. Defaults to `0`. */
    initialHeight?: number;
};
/**
 * The `Size` animation changes the width or height of an element.
 */
declare const Size: (options: SizeOptions) => Animation;
export default Size;
//# sourceMappingURL=Size.d.ts.map