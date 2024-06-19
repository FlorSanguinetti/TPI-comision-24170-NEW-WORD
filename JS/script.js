/*repite header y footer en todas las hojas*/
let header =
    `<div class="header-logo"><a href="Index.html"><img class="logo" src="/img/Logo new word2 (1).png" alt="logo"><span id="newWord"><h5>New Word</h5></span></a>
</div>

<input class="checkbox" type="checkbox">
<img class="icono hamburguesa" src="/img/menu-burger.png" alt="Abrir">
<img class="icono cruz" src="/img/cross.png" alt="Cerrar">
<ul class="lista">
    <li> <a href="index.html">Inicio</a></li>
    <li><a href="/cursos.html">Cursos</a></li>
    <li><a href="/nosotros.html">Nosotros</a></li>
    <li><a href="contacto.html">Contacto</a></li>
</ul>`; document.getElementById("idheader").innerHTML = header;

let footer = `<div>
<div class="footerContacto">
    <div id="footerDireccion">
        <h5>SEDE CENTRAL</h5>
        <H5>Av. Callao 556</H5>
        <h5>Tel. 5452-6595</h5>
        
        <span><i class="fa-brands fa-whatsapp"></i><h5 style="margin-left: 1em;">+54911857462</h5></span>
        
        <span><i class="fa-brands fa-instagram"></i></i><h5 style="margin-left: 1em;">@new_word</h5></span>
        
        <span><i class="fa-regular fa-envelope"></i>
        <h5 style="margin-left: 1em;">info@newword.com</h5> </span>
    </div>
</div>    
<div><iframe id="iframe" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3284.065089821167!2d-58.39530572350354!3d-34.60251555743609!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x95bccac04fbb666d%3A0xd0c6b20328d58297!2sAv.%20Callao%20556%2C%20C1022AAS%20Cdad.%20Aut%C3%B3noma%20de%20Buenos%20Aires%2C%20Argentina!5e0!3m2!1sen!2ses!4v1715956044211!5m2!1sen!2ses" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></iframe></div>

</div> <h7 id="copyright">Copyright 2024. Todos los derechos reservados</h7>`; document.getElementById("footer").innerHTML = footer;

