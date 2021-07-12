function deleteTask(taskId) {
            axios.post(`/delete-to-do/${taskId}`, {
                'taskToDelete': taskId,
            }).then((response) => {
                console.log(response);
                if (response.status === 200) {
                    let result = document.querySelectorAll(`.id_${taskId}`);
                    result.forEach(el => el.remove());
                }
            })

        }