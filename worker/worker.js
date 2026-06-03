/**
 * Grenadier OBD2 – Alpha Tester signup proxy
 * Forwards form submissions to BetterStack log ingestion.
 *
 * Deploy:
 *   wrangler deploy
 *
 * Set secret:
 *   wrangler secret put BETTERSTACK_TOKEN
 */

const BETTERSTACK_URL = 'https://in.logs.betterstack.com';

function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin':  origin ?? '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin');

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }

    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return new Response('Invalid JSON', { status: 400, headers: corsHeaders(origin) });
    }

    // Forward to BetterStack
    const res = await fetch(BETTERSTACK_URL, {
      method:  'POST',
      headers: {
        'Content-Type':  'application/json',
        'Authorization': 'Bearer ' + env.BETTERSTACK_TOKEN,
      },
      body: JSON.stringify({
        ...body,
        forwarded_at: new Date().toISOString(),
      }),
    });

    const status = res.ok ? 200 : 502;
    return new Response(null, { status, headers: corsHeaders(origin) });
  },
};
