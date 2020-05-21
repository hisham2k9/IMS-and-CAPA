function GetDays()
{
    var dropdt = new Date(document.getElementById("id_patienttrack_1").value);
    alert(dropdt)
    var pickdt = new Date(document.getElementById("id_patienttrack_2").value);
    return parseInt((dropdt - pickdt) / (24 * 3600 * 1000));
}

function cal()
{
    if(document.getElementById("id_patienttrack_1"))
    {
    document.getElementById("id_patienttrack_3").value=GetDays();
    }
}