function list_qr() {
    let $ = django.jQuery;
    console.log("list QR")
}

function getKabupaten(prov_id) {
    console.log(prov_id)
    let $ = django.jQuery;
    $.get('/api/address/kota/' + prov_id, function (resp){
        let kabupaten_list = '<option value="" selected="">---------</option>'
        console.log(resp.data.results)
        $.each(resp.data.results, function(i, item){
            kabupaten_list += '<option value="'+ item.id +'">'+ item.name  +'</option>'
        });
        $('#id_kota').html(kabupaten_list);
    });
}

function getGedung(instansi_id) {
    let $ = django.jQuery;
    $.get('/api/instansi/gedung/' + instansi_id, function (resp){
        let gedung_list = '<option value="" selected="">---------</option>'
        $.each(resp.data.results, function(i, item){
            gedung_list += '<option value="'+ item.id +'">'+ item.name +  " -> " + item.instansi.name +'</option>'
        });
        $('#id_gedung').html(gedung_list);
    });
}

function getRuang(gedung_id) {
    let $ = django.jQuery;
    $.get('/api/instansi/ruang/' + gedung_id, function (resp){
        let runag_list = '<option value="" selected="">---------</option>'
        $.each(resp.data.results, function(i, item){
            runag_list += '<option value="'+ item.id +'">'+ item.name + " -> " + item.gedung.name +'</option>'
            console.log(item.gedung.name)
        });
        $('#id_ruang').html(runag_list);
    });
}
