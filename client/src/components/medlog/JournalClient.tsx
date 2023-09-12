"use client";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Dispatch, SetStateAction, useState } from "react";

const MOODDESC_KEY = "mooddesc";

type MoodDescResp = {
    success: boolean;
    payload?: {
        body: string;
    };
};

function changeDate(isostr: string, change: number) {
    let d = new Date(isostr);
    d.setDate(d.getDate() + change);
    return d.toISOString().split("T")[0];
}

function DateButton({
    kind,
    date,
    setDate,
    today,
}: {
    kind: "back" | "forward";
    date: string;
    setDate: Dispatch<SetStateAction<string>>;
    today: string;
}) {
    const isForward = kind === "forward";
    return (
        <button
            className={`button ${
                date == today && isForward
                    ? "text-gray-300 cursor-auto"
                    : "text-black cursor-pointer"
            }`}
            disabled={date == today && isForward}
            onClick={() => {
                setDate(changeDate(date, isForward ? 1 : -1));
            }}
        >
            {isForward ? "Forward" : "Back"}
        </button>
    );
}

type JournalProps = {
    className?: string;
    today: string;
};

export default function Journal({ today, className }: JournalProps) {
    const [date, setDate] = useState(today);
    // value of textarea
    const [value, setValue] = useState("Loading...");
    const queryClient = useQueryClient();
    const { data } = useQuery({
        queryKey: [MOODDESC_KEY, date],
        queryFn: async () => {
            const req = new Request(
                "/api/log/mooddesc?" +
                    new URLSearchParams({
                        date,
                    })
            );
            const res = (await (await fetch(req)).json()) as MoodDescResp;
            // this does introduce another render cycle but shouldnt redo
            // the query as nothing in the key has changed
            setValue(res?.payload?.body ?? "");
            return res;
        },
    });
    return (
        <section className={className ?? ""}>
            <h1>{date}</h1>
            <div className="flex align-middle items-center">
                <DateButton
                    kind="back"
                    date={date}
                    setDate={setDate}
                    today={today}
                />
                <form
                    className="text-center grow px-4"
                    onSubmit={(e) => {
                        e.preventDefault(); // prevents reload
                        const formData = new FormData(
                            e.target as HTMLFormElement
                        );
                        formData.set("date", date);
                        const req = new Request("/api/log/mooddesc", {
                            method: "PUT",
                            body: formData,
                        });
                        fetch(req);
                        queryClient.invalidateQueries([MOODDESC_KEY]);
                    }}
                >
                    <label className="bg-red-400">
                        Description:
                        <textarea
                            className="block border-black border-2 w-full h-1/2 p-2 my-2"
                            name="desc"
                            value={value}
                            onChange={(e) => setValue(e.target.value)}
                        />
                    </label>
                    <button type="submit" className="button">
                        Save
                    </button>
                </form>
                <DateButton
                    kind="forward"
                    date={date}
                    setDate={setDate}
                    today={today}
                />
            </div>
        </section>
    );
}
