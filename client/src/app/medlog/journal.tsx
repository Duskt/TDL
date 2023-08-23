"use client";
import query from "@/query";

type Props = {
    defaultValue: string;
}

export default function Journal({ defaultValue, }: Props) {
    return (
    <form onSubmit={
            (e) => {
                e.preventDefault(); // prevents reload
                const form = e.target as HTMLFormElement;
                /*query({path: '/api/log/mooddesc',
                    method: 'PUT', 
                    body: new FormData(form),
                }, ['mooddesc-today'])*/
                const req = new Request("/api/log/mooddesc", {
                    method: "PUT",
                    body: new FormData(form)
                });
                fetch(req)
                console.log("Success")
            }}>
        <label>Description:
            <textarea className="block" name="desc" defaultValue={defaultValue} />
        </label>
        <button type="submit">Save</button>
    </form>
    );
}