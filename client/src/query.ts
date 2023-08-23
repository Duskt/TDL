import { RequestInit } from "next/dist/server/web/spec-extension/request"

interface Query {
    path: string,
    searchParams?: {
        [key: string]: string
    },
    method?: RequestInit['method']
    body?: RequestInit['body']
}

export default async function query<T>({
    path,
    searchParams,
    method,
    body,
}: Query, tags?: string[]): Promise<T> {
    if (!path.startsWith('/')) {
        path = `/${path}`
    }
    let qp = ""
    if (searchParams) {
        qp = '?'+ new URLSearchParams(searchParams)
    }

    let req
    if (typeof window !== 'undefined') {
        // client - can create request without host or port
        req = new Request(path+qp, {method, body, cache: 'no-cache'})
    } else {
        // server - private env variables should exist
        const host = process.env.HOST
        if (host === undefined) {
            throw Error(`HOST not found in ${process.env}`)
        }
        const api_port = process.env.API_PORT
        if (api_port === undefined) {
            throw Error(`API_PORT not found`)
        }
        req = new Request(new URL(`http://${host}:${api_port}${path}`)+qp, {method, body, cache: 'no-cache'})
    }
    console.log("Requesting...")
    const res = await fetch(req);
    return await res.json() as T
}