import { interpolate } from 'remotion';
const DEFAULT_DURATION = 15;
const CustomEasing = (easingFunction) => (frame, _fps, options = {}) => {
    var _a;
    const { start } = options;
    const durationInFrames = (_a = options.duration) !== null && _a !== void 0 ? _a : DEFAULT_DURATION;
    const driver = interpolate(frame - (start !== null && start !== void 0 ? start : 0), [0, durationInFrames], [0, 1], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
        easing: easingFunction,
    });
    return { driver };
};
export default CustomEasing;
