/**
 * The URL of the Python server.
 */
const URL = "http://127.0.0.1:5001";

export function params(
  init?: ConstructorParameters<typeof URLSearchParams>[0]
): string {
  return new URLSearchParams(init).toString();
}

export function fetchWrapper(path: string, init?: RequestInit) {
  return fetch(`${URL}${path}`, init);
}

/**
 * A wrapper around `fetch` that prepends the URL of the Python server.
 */
export async function fetchJson(path: string, init?: RequestInit) {
  const response = await fetchWrapper(path, init);

  if (!response.ok) {
    throw new Error(response.statusText);
  }

  try {
    const json: unknown = await response.json();
    return json;
  } catch (error: unknown) {
    throw new Error(error as string);
  }
}
