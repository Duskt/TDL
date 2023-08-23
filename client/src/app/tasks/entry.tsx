import { useState } from "react"
import React from "react"

interface EntryProps {
    title: string,
    description: string,
    done: boolean
}

const Entry: React.FC<EntryProps> = (
    { title, description, done }
) => {
    const [selected, setSelected] = useState(done);
    return <tr>
        <td>{title}</td>
        <td>{description}</td>
        <td><input type="checkbox" checked={selected} onClick={() => setSelected(!selected)}/></td>
    </tr>
}
export default Entry