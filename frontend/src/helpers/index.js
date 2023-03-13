export const debounce = (fn, delay = 10) => {
  let timeoutId = null;

  return () => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(fn, delay);
  };
};
