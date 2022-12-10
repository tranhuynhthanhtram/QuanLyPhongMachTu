function pay(id){
    if(confirm("Bạn có chắc thanh toán?") == true)
    {
        fetch('/api/pay',{
            method: 'post',
            body: JSON.stringify({
                'id': id,
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            console.info(data)
            if(data.code == 200){
                location.reload()
            }
        }).catch(err => console.error(err))
    }
}
