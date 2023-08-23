import { useEffect, useState } from "react";
import Entry from "./entry";

interface Task {
    title: string,
    description: string,
    done: boolean,
    instance_id: number
}

const TaskCalendar = () => {
    const [tasks, setTasks] = useState<Task[]>([]);
    
    useEffect(()=>{
        async function fetchTasks() {
            const respJson = await (await fetch("/api/tasks/today")).json();
            setTasks(respJson.payload);
        }
        fetchTasks()
    }, []);
    return (<table>
        <tbody>
            <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Done?</th>
            </tr>
            {tasks.map(
                (i) => <Entry key={i.instance_id} title={i.title} description={i.description} done={i.done}/>
            )}
        </tbody>
    </table>
    );
}

export default TaskCalendar;