function deleteTask(taskId) {
            axios.post(`/delete-to-do/${taskId}`, {
                'taskToDelete': taskId,
            }).then((response) => {
                if (response.status === 200) {
                    let result = document.querySelector(`#id_${taskId}`).remove();
                }
            })

        }