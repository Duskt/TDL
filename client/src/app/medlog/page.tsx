import Journal from "./journal";
import query from "@/query";

type MoodDescResp = {
    success: boolean
    payload?: {
        body: string
    }
}

export default async function MedLog() {
    const today = new Date().toISOString().split('T')[0];
    const [host, api_port] = [process.env.HOST, process.env.API_PORT];
    const req = new Request(`http://${host}:3000/api/log/mooddesc?` + new URLSearchParams({
        'date': today
    }));
    const res = await fetch(req, { next: {tags: ['mooddesc-today']}})
    console.log("Fetching ", req.url)
    const payload = (await res.json() as MoodDescResp).payload
    // const res = await query<MoodDescResp>({path: '/api/log/mooddesc', searchParams: {
    //     'date': today
    // }}, ['mooddesc-today'])
    return <Journal defaultValue={payload?.body ?? "ERR"}></Journal>
}