import { type Ref, nextTick } from 'vue';
import { computedAsync } from '@vueuse/core';
import { User } from './types';
import { router } from './router';
import {
  parseCreationOptionsFromJSON,
  create as webauthnCreate,
  get as webauthnGet,
  parseRequestOptionsFromJSON,
} from '@github/webauthn-json/browser-ponyfill';

// pull out promise so we can await it in isAuth
const userPromise: Promise<User | null> = fetch(`${import.meta.env.VITE_SERVER_ADDR}/user/info`, {
  credentials: 'include',
}).then((res) => (res.ok ? res.json() : null));

export const user: Ref<User | null> = computedAsync(async () => await userPromise, null);

export async function getUser() {
  await userPromise;
  await nextTick();
  return user.value;
}

export async function updateUser() {
  const response = await fetch(`${import.meta.env.VITE_SERVER_ADDR}/user/update`, {
    credentials: 'include',
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify(user.value),
  });
  const json = await response.json();
  if (!response.ok) {
    throw new Error(json.error);
  }
  user.value = json;
}

// Auth
export async function isAuth() {
  return (await getUser()) !== null;
}

export async function logout() {
  await fetch(`${import.meta.env.VITE_SERVER_ADDR}/user/logout`, {
    method: 'POST',
    credentials: 'include',
  });
  user.value = null;
  document.cookie = 'session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  if (router.currentRoute.value.meta.auth) {
    await router.push('/');
  }
}

export async function login(username: string) {
  const response = await fetch(`${import.meta.env.VITE_SERVER_ADDR}/user/login`, {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      username: username.trim(),
    }),
  });
  const json = await response.json();
  if (!response.ok) {
    throw new Error(json.error);
  }
  const id: string = json.id;
  const gco = parseRequestOptionsFromJSON({
    publicKey: json.options,
  });

  const webauthResp = await webauthnGet(gco).catch(() => {
    throw new Error('Authentication canceled');
  });

  const verifyResp = await fetch(`${import.meta.env.VITE_SERVER_ADDR}/user/login_verify`, {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      resp: webauthResp.toJSON(),
      id,
    }),
  });

  const verifyJson = await verifyResp.json();
  if (!verifyResp.ok) {
    throw new Error(verifyJson.error);
  }
  user.value = verifyJson.user;
  document.cookie = `session=${verifyJson.session}`;
  return user.value;
}

export async function register(username: string, name: string) {
  const response = await fetch(`${import.meta.env.VITE_SERVER_ADDR}/user/register`, {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      name: name.trim(),
      username: username.trim(),
    }),
  });
  const json = await response.json();
  if (!response.ok) {
    throw new Error(json.error);
  }
  const id: string = json.id;
  const cco = parseCreationOptionsFromJSON({
    publicKey: json.options,
  });

  delete cco.publicKey?.attestation;
  delete cco.publicKey?.rp.id;

  const webauthResp = await webauthnCreate(cco).catch(() => {
    throw new Error('Registration canceled');
  });

  const verifyResp = await fetch(`${import.meta.env.VITE_SERVER_ADDR}/user/register_verify`, {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      resp: webauthResp.toJSON(),
      id,
    }),
  });

  const verifyJson = await verifyResp.json();
  if (!verifyResp.ok) {
    throw new Error(verifyJson.error);
  }
  user.value = verifyJson.user;
  document.cookie = `session=${verifyJson.session}`;
}
