const CURRENT = 'current';

export function getCurrentUser() {
  return JSON.parse(window.localStorage.getItem(CURRENT));
}

export function setCurrentUser(user) {
  window.localStorage.setItem(CURRENT, JSON.stringify(user));
}

export function clearCurrentUser() {
  window.localStorage.removeItem(CURRENT);
}