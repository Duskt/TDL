import { revalidatePath, revalidateTag } from "next/cache";
import { NextRequest, NextResponse } from "next/server";
// todo - use asynchronous key encryption to make sure all requests
// are from a non-malicious client? apparently this is most important
// when revalidating

const PORT = process.env.API_PORT as string;

export async function GET(req: NextRequest) {
    const redir = new URL(req.url);
    redir.port = PORT;
    console.log("Redirected GET");
    return await fetch(redir);
}

export async function POST(req: NextRequest) {
    console.log("\nRoute handler redirected POST.\n");
    const redir = new URL(req.url);
    redir.port = PORT;
    return await fetch(redir);
}

export async function PUT(req: NextRequest) {
    console.log("\nRoute handler redirected PUT\n");

    const redir_url = new URL(req.url);
    redir_url.port = PORT;
    const redir = new NextRequest(redir_url, req);

    if (redir.nextUrl.pathname.includes("log")) {
        console.log("Revalidating...");
        revalidatePath("/medlog");
    }
    return await fetch(redir);
}
