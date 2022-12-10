function addToCart(i){
    let x = document.getElementsByClassName("medicine");
    let unit = document.getElementsByClassName("unit");
    let how_to_use = document.getElementsByClassName("how_to_use");

    id = x[i].value//mã thuốc
    if(id != 0)
    {
        fetch('/api/add-medicine-to-cart',{
        method: 'post',
        body: JSON.stringify({
            'id': id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
        }).then(res => res.json()).then(data => {
            console.info(data)
            if(data.unit_id == '1'){
                unit[i].innerHTML =  `<span>Chai</span>`
            }
             if(data.unit_id == '2'){
                unit[i].innerHTML =  `<span>Vỹ</span>`
            }
             if(data.unit_id == '3'){
                unit[i].innerHTML =  `<span>Viên</span>`
            }

            how_to_use[i].innerHTML = data.how_to_use

       }).catch(err => console.error(err))
   }
   else
   {
    console.log('id = 0')
   }
}

function updateQuantity(line, obj){
    var x = document.getElementsByClassName("medicine");
    id = x[line].value

    console.log(id)
    console.log(obj.value)

    if(id){
        fetch('/api/update-quantity',{
        method: 'put',
        body: JSON.stringify({
            'id': id,
            'quantity': parseInt(obj.value)
       }),
        headers: {
            'Content-Type': 'application/json'
        }
        }).then(res => res.json()).then(data => {
            console.info(data)
            if(data.code == 200){
                console.log("Thành công")
            }
       }).catch(err => console.error(err))
    }
    else
    {
      console.log("Không lấy được id")
    }
}

function deleteMedicineCart(line){
    var x = document.getElementsByClassName("medicine");
    id = x[line].value

    if(id){
        if(confirm("Bạn có muốn xóa không?") == true){
            fetch('/api/delete-medicine-cart',{
            method: 'delete',
             body: JSON.stringify({
            'id': id
       }),
        headers: {
            'Content-Type': 'application/json'
        }
            }).then(res => res.json()).then(data => {
                console.info(data)

                let r = document.getElementById(`cart${id}`)
                r.style.display = "none"

                if(data.code == 200){
                    console.log("Thành công")
                }
           }).catch(err => console.error(err))
        }
    }
    else
    {
      console.log("Không lấy được id")
    }
}

function saveMedicalBill(){
    if(confirm("Bạn có muốn lưu phiếu?") == true)
    {
        fetch('/add-phieu-kham',{
        method: 'post'
        }).then(res => res.json()).then(data => {
            console.info(data)
            if(data.code == 200){
                alert("Lưu phiếu khám thành công");
            }
            else
                alert("Hệ thống bị lỗi");
        }).catch(err => console.error(err))
    }
}

function searchMedicalHistory(){
     let fullname=document.getElementById("fullname").value;
     fetch('/api/search-medical-history',{
        method: 'post',
        body: JSON.stringify({
            'fullname': fullname
       }),
        headers: {
            'Content-Type': 'application/json'
        }
        }).then(res => res.json()).then(data => {
            console.info(data)
                let name=document.getElementsByClassName("name")
                for(let i=0; i<name.length; i++)
                    name[i].innerText=data.name[i]
                let quantity=document.getElementsByClassName("quantity")
                for(let i=0; i<quantity.length; i++)
                    quantity[i].innerText=data.quantity[i]
       }).catch(err => console.error(err))
}
