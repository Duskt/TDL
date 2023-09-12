import { Url } from "next/dist/shared/lib/router/router";
import Link from "next/link";

export interface NavbarTab {
    page_id: string;
    title: string;
    redirect: Url;
}

interface NavbarProps {
    tabs: NavbarTab[];
}

export default function Navbar({ tabs }: NavbarProps) {
    return (
        <nav className="border-b border-black mb-4 p-2 flex justify-around">
            {tabs.map(({ page_id, title, redirect }) => (
                <Link
                    key={page_id}
                    className="border border-black rounded-md px-1"
                    href={redirect}
                    prefetch={false}
                >
                    {title}
                </Link>
            ))}
        </nav>
    );
}
