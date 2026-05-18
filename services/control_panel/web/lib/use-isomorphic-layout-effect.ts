import { useEffect, useLayoutEffect } from "react";

// useLayoutEffect, but degrades to useEffect during SSR (where there's no DOM
// and React would otherwise warn). Use this to apply localStorage-persisted UI
// preferences *before* the browser paints — eliminating the one-frame flash
// where the default state shows before the stored one is read.
export const useIsomorphicLayoutEffect =
  typeof window !== "undefined" ? useLayoutEffect : useEffect;
