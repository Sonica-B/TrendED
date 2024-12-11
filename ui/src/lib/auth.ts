import { Ref } from 'vue';
import { computedAsync } from '@vueuse/core';
import { User } from './types';
import { router } from './router';

// pull out promise so we can await it in isAuth
const userPromise = async () => {
  const res = await fetch(`${import.meta.env.VITE_SERVER_ADDR}/auth/user`, {
    credentials: 'include',
  });
  if (res.ok) {
    return await res.json();
  } else {
    return null;
  }
};
export const user: Ref<User | null> = computedAsync(userPromise, null);

export async function isAuth() {
  await userPromise();
  return user.value !== null;
}

export async function logout() {
  await fetch(`${import.meta.env.VITE_SERVER_ADDR}/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  });
  user.value = null;
  document.cookie = 'session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  if (router.currentRoute.value.meta.auth) {
    await router.push('/');
  }
}

import {
  parseCreationOptionsFromJSON,
  create as webauthnCreate,
  get as webauthnGet,
  parseRequestOptionsFromJSON,
} from '@github/webauthn-json/browser-ponyfill';

export async function login(username: string) {
  const response = await fetch(`${import.meta.env.VITE_SERVER_ADDR}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      username,
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
  console.log('gco', gco);

  const webauthResp = await webauthnGet(gco).catch(() => {
    throw new Error('Authentication canceled');
  });

  console.log('webauthGetResp', webauthResp);

  const verifyResp = await fetch(`${import.meta.env.VITE_SERVER_ADDR}/auth/login_verify`, {
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
  console.log('Verify Json', verifyJson);
  document.cookie = `session=${verifyJson.session}`;
  return user.value;
}
export async function register(username: string, name: string) {
  const response = await fetch(`${import.meta.env.VITE_SERVER_ADDR}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      name,
      username,
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
  console.log('cco', cco);

  delete cco.publicKey?.attestation;
  delete cco.publicKey?.rp.id;

  const webauthResp = await webauthnCreate(cco).catch(() => {
    throw new Error('Registration canceled');
  });

  console.log('webauthCreateResp', webauthResp);
  const verifyResp = await fetch(`${import.meta.env.VITE_SERVER_ADDR}/auth/register_verify`, {
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
  console.log('Verify Json Reg', verifyJson);
  document.cookie = `session=${verifyJson.session}`;
}
