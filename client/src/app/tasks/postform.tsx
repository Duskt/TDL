const PostForm = () => {
    return <form action="/api/tasks/taskclass" method="post">
        <label htmlFor="title">Title:</label>
        <input type="text" id="title" name="title" />

        <label htmlFor="description">Description:</label>
        <textarea id="description" name="description"></textarea>

        <button type="submit">Submit</button>
    </form>;
}

export default PostForm;