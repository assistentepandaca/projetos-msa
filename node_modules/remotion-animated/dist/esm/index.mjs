// src/Animated.tsx
import { useMemo } from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";

// src/reducer/ReductionStrategy.ts
var reductionStrategyForProperty = (property) => {
  switch (property) {
    case "translateX":
    case "translateY":
    case "translateZ":
    case "rotateX":
    case "rotateY":
    case "rotateZ":
      return 0 /* Addition */;
    case "scaleX":
    case "scaleY":
    case "scaleZ":
      return 1 /* Multiplication */;
    case "opacity":
    case "width":
    case "height":
    default:
      return 2 /* IgnorePreviousValue */;
  }
};
var ReductionStrategy_default = reductionStrategyForProperty;

// src/reducer/AnimationReducer.ts
var reduceComputedValues = (valueLists) => valueLists.reduce((acc, valueList) => {
  const properties = Object.keys(valueList);
  const reducedValues = { ...acc };
  properties.forEach((property) => {
    let reducedValue = valueList[property];
    if (acc[property] !== undefined && reducedValue !== undefined) {
      reducedValue = reduceValue(property, reducedValue, acc);
    }
    reducedValues[property] = reducedValue;
  });
  return reducedValues;
}, {});
function reduceValue(property, reducedValue, acc) {
  const strategy = ReductionStrategy_default(property);
  switch (strategy) {
    case 0 /* Addition */:
      return (acc[property] ?? 0) + (reducedValue ?? 0);
    case 1 /* Multiplication */:
      return (acc[property] ?? 1) * (reducedValue ?? 1);
    case 2 /* IgnorePreviousValue */:
    default:
      return reducedValue;
  }
}
var AnimationReducer_default = reduceComputedValues;

// src/styles/TransformStyles.ts
var value = (currentValue, defaultValue) => currentValue === undefined ? defaultValue : currentValue.toFixed(4);
var transformStyles = (values) => {
  let translate;
  let scale;
  let rotateX;
  let rotateY;
  let rotateZ;
  if (values.translateX || values.translateY || values.translateZ) {
    const translateX = `${value(values.translateX, 0)}px`;
    const translateY = `${value(values.translateY, 0)}px`;
    const translateZ = `${value(values.translateZ, 0)}px`;
    translate = `translate3d(${translateX}, ${translateY}, ${translateZ})`;
  }
  if (values.scaleX !== undefined || values.scaleY !== undefined || values.scaleZ !== undefined) {
    const scaleX = value(values.scaleX, 1);
    const scaleY = value(values.scaleY, 1);
    const scaleZ = value(values.scaleZ, 1);
    scale = `scale3d(${scaleX}, ${scaleY}, ${scaleZ})`;
  }
  if (values.rotateX)
    rotateX = `rotateX(${value(values.rotateX, 0)}deg)`;
  if (values.rotateY)
    rotateY = `rotateY(${value(values.rotateY, 0)}deg)`;
  if (values.rotateZ)
    rotateZ = `rotateZ(${value(values.rotateZ, 0)}deg)`;
  if (!translate && !scale && !rotateX && !rotateY && !rotateZ) {
    return null;
  }
  let transform = "";
  if (translate)
    transform += translate;
  if (scale)
    transform += ` ${scale}`;
  if (rotateX)
    transform += ` ${rotateX}`;
  if (rotateY)
    transform += ` ${rotateY}`;
  if (rotateZ)
    transform += ` ${rotateZ}`;
  return transform.trim();
};
var TransformStyles_default = transformStyles;

// src/styles/AnimatedStyles.ts
var stylesFromValues = (values) => {
  const properties = {};
  const transform = TransformStyles_default(values);
  if (values.opacity !== undefined)
    properties.opacity = values.opacity;
  if (values.width !== undefined)
    properties.width = values.width;
  if (values.height !== undefined)
    properties.height = values.height;
  if (transform)
    properties.transform = transform;
  return properties;
};
var AnimatedStyles_default = stylesFromValues;

// src/Animated.tsx
import { jsx } from "react/jsx-runtime";
var animatedStylesFromAnimations = (animations, currentFrame, fps) => {
  const currentAnimations = animations.filter((animation) => animation.in <= currentFrame);
  const computedValues = currentAnimations.map((animation) => animation.valuesAt(currentFrame, fps) ?? {});
  const animatedValues = AnimationReducer_default(computedValues);
  return AnimatedStyles_default(animatedValues);
};
var Animated = (props) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { animations } = props;
  const animationFrame = frame - (props.delay ?? 0);
  const animatedStyles = useMemo(() => animatedStylesFromAnimations(animations, animationFrame, fps), [animationFrame, fps, animations]);
  const isBeforeInPoint = props.in && frame < props.in;
  const isAfterOutPoint = props.out && frame > props.out;
  if (isBeforeInPoint || isAfterOutPoint) {
    return null;
  }
  return /* @__PURE__ */ jsx("div", {
    className: props.className,
    style: {
      ...props.style,
      ...animatedStyles,
      position: props.absolute ? "absolute" : undefined
    },
    children: props.children
  });
};
var Animated_default = Animated;

// src/easing/behaviours/CustomSpring.ts
import { spring } from "remotion";
var CustomSpring = (withDefaultConfig) => (frame, fps, options = {}) => {
  const { start, ...overrideSpringConfig } = options;
  const driver = spring({
    fps,
    frame: frame - (start ?? 0),
    durationInFrames: options.duration,
    config: {
      ...withDefaultConfig,
      ...overrideSpringConfig
    }
  });
  return { driver };
};
var CustomSpring_default = CustomSpring;

// src/easing/behaviours/DefaultSpring.ts
var DefaultSpring = CustomSpring_default({
  stiffness: 75,
  damping: 200,
  overshootClamping: true
});
var DefaultSpring_default = DefaultSpring;

// src/easing/EasingBehaviour.ts
var easingForOptions = (options, defaultingTo = DefaultSpring_default) => {
  if ("ease" in options && typeof options.ease === "function")
    return options.ease;
  return defaultingTo;
};
var valueWithEasing = (frame, fps, options, defaultingTo = DefaultSpring_default) => {
  const easingFunction = easingForOptions(options, defaultingTo);
  const value2 = easingFunction(frame, fps, options);
  if (value2.driver === undefined) {
    throw new TypeError("Easing function must return a driver value. You may have imported an easing function from Remotion directly, rather than from the `Ease` collection of `remotion-animated`. If you intended to use a Remotion easing function directly, wrap it with the `CustomEasing` function first.");
  }
  return value2.driver;
};

// src/animations/AnimationInterpolation.ts
import { interpolate } from "remotion";
var interpolateAnimation = (input, to, initialValue = 0, defaultValue = initialValue, clamp = false) => {
  if (to === undefined)
    return defaultValue;
  return interpolate(input, [0, 1], [initialValue, to], {
    extrapolateLeft: clamp ? "clamp" : undefined,
    extrapolateRight: clamp ? "clamp" : undefined
  });
};
var AnimationInterpolation_default = interpolateAnimation;

// src/animations/Fade.ts
var Fade = (options) => {
  const start = options.start ?? 0;
  return {
    in: start,
    valuesAt: (frame, fps) => {
      const input = valueWithEasing(frame, fps, options);
      const initial = options.initial ?? 1;
      const opacity = AnimationInterpolation_default(input, options.to, initial, initial, true);
      return { opacity };
    }
  };
};
var Fade_default = Fade;

// src/animations/Move.ts
var Move = (options) => {
  return {
    in: options.start ?? 0,
    valuesAt: (frame, fps) => {
      const input = valueWithEasing(frame, fps, options);
      const translateX = AnimationInterpolation_default(input, options.x, options.initialX);
      const translateY = AnimationInterpolation_default(input, options.y, options.initialY);
      const translateZ = AnimationInterpolation_default(input, options.z, options.initialZ);
      return { translateX, translateY, translateZ };
    }
  };
};
var Move_default = Move;

// src/animations/Rotate.ts
var Rotate = (options) => {
  return {
    in: options.start ?? 0,
    valuesAt: (frame, fps) => {
      const input = valueWithEasing(frame, fps, options);
      const initialX = options.initialX ?? 0;
      const initialY = options.initialY ?? 0;
      const initialZ = options.initial ?? 0;
      const rotateX = AnimationInterpolation_default(input, options.degreesX, initialX);
      const rotateY = AnimationInterpolation_default(input, options.degreesY, initialY);
      const rotateZ = AnimationInterpolation_default(input, options.degrees, initialZ);
      return { rotateX, rotateY, rotateZ };
    }
  };
};
var Rotate_default = Rotate;

// src/animations/Scale.ts
var Scale = (options) => {
  return {
    in: options.start ?? 0,
    valuesAt: (frame, fps) => {
      const input = valueWithEasing(frame, fps, options);
      const initial = options.initial ?? 1;
      const initialX = options.initialX ?? initial;
      const initialY = options.initialY ?? initial;
      const initialZ = options.initialZ ?? initial;
      const scaleX = AnimationInterpolation_default(input, options.x ?? options.by, initialX);
      const scaleY = AnimationInterpolation_default(input, options.y ?? options.by, initialY);
      const scaleZ = AnimationInterpolation_default(input, options.z, initialZ);
      return { scaleX, scaleY, scaleZ };
    }
  };
};
var Scale_default = Scale;

// src/animations/Size.ts
var Size = (options) => {
  return {
    in: options.start ?? 0,
    valuesAt: (frame, fps) => {
      const values = {};
      const input = valueWithEasing(frame, fps, options);
      if (options.width)
        values.width = AnimationInterpolation_default(input, options.width, options.initialWidth);
      if (options.height)
        values.height = AnimationInterpolation_default(input, options.height, options.initialHeight);
      return values;
    }
  };
};
var Size_default = Size;

// src/easing/behaviours/CustomEasing.ts
import { interpolate as interpolate2 } from "remotion";
var DEFAULT_DURATION = 15;
var CustomEasing = (easingFunction) => (frame, _fps, options = {}) => {
  const { start } = options;
  const durationInFrames = options.duration ?? DEFAULT_DURATION;
  const driver = interpolate2(frame - (start ?? 0), [0, durationInFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: easingFunction
  });
  return { driver };
};
var CustomEasing_default = CustomEasing;

// src/easing/behaviours/Ease.ts
import { Easing } from "remotion";
var Ease;
((Ease) => {
  Ease.Linear = CustomEasing_default(Easing.linear);
  Ease.QuadraticIn = CustomEasing_default(Easing.in(Easing.quad));
  Ease.QuadraticOut = CustomEasing_default(Easing.out(Easing.quad));
  Ease.QuadraticInOut = CustomEasing_default(Easing.inOut(Easing.quad));
  Ease.CubicIn = CustomEasing_default(Easing.in(Easing.cubic));
  Ease.CubicOut = CustomEasing_default(Easing.out(Easing.cubic));
  Ease.CubicInOut = CustomEasing_default(Easing.inOut(Easing.cubic));
  Ease.QuarticIn = CustomEasing_default(Easing.in(Easing.poly(4)));
  Ease.QuarticOut = CustomEasing_default(Easing.out(Easing.poly(4)));
  Ease.QuarticInOut = CustomEasing_default(Easing.inOut(Easing.poly(4)));
  Ease.QuinticIn = CustomEasing_default(Easing.in(Easing.poly(5)));
  Ease.QuinticOut = CustomEasing_default(Easing.out(Easing.poly(5)));
  Ease.QuinticInOut = CustomEasing_default(Easing.inOut(Easing.poly(5)));
  Ease.SinusoidalIn = CustomEasing_default(Easing.in(Easing.sin));
  Ease.SinusoidalOut = CustomEasing_default(Easing.out(Easing.sin));
  Ease.SinusoidalInOut = CustomEasing_default(Easing.inOut(Easing.sin));
  Ease.CircularIn = CustomEasing_default(Easing.in(Easing.circle));
  Ease.CircularOut = CustomEasing_default(Easing.out(Easing.circle));
  Ease.CircularInOut = CustomEasing_default(Easing.inOut(Easing.circle));
  Ease.ExponentialIn = CustomEasing_default(Easing.in(Easing.exp));
  Ease.ExponentialOut = CustomEasing_default(Easing.out(Easing.exp));
  Ease.ExponentialInOut = CustomEasing_default(Easing.inOut(Easing.exp));
  Ease.BounceIn = CustomEasing_default(Easing.in(Easing.bounce));
  Ease.BounceOut = CustomEasing_default(Easing.out(Easing.bounce));
  Ease.BounceInOut = CustomEasing_default(Easing.inOut(Easing.bounce));
  Ease.Bezier = (x1, y1, x2, y2) => CustomEasing_default(Easing.bezier(x1, y1, x2, y2));
})(Ease ||= {});
var Ease_default = Ease;
export {
  Ease_default as TimingFunctions,
  Size_default as Size,
  Scale_default as Scale,
  Rotate_default as Rotate,
  Move_default as Move,
  Fade_default as Fade,
  Ease_default as Ease,
  CustomEasing_default as CustomEasing,
  Animated_default as Animated
};
