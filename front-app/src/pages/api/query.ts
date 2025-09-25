import type { NextApiRequest, NextApiResponse } from "next";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL
type Data = { result: unknown };

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data | { error: string }>

// since only post request is allowed
) {
  if (req.method !== "POST") {
    res.setHeader("Allow", ["POST"]);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }

  try {
    if (!BACKEND_URL) {
      return res.status(500).json({ error: "BACKEND_URL is not defined" });
    }

    const backendResponse = await fetch(`${BACKEND_URL}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: req.body,
    });

    const data: Data = await backendResponse.json();
    res.status(200).json(data);
  } catch (error) {
    res.status(500).json({ error: "Failed to process query" });
  }
}
