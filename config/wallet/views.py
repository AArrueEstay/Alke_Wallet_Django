from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Transaccion
from decimal import Decimal


# DASHBOARD
def dashboard(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    transacciones = Transaccion.objects.filter(usuario=usuario)

    return render(request, 'dashboard.html', {
        'usuario': usuario,
        'transacciones': transacciones
    })


# CREAR USUARIO
def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']

        # 🔥 VALIDACIÓN
        if Usuario.objects.filter(email=email).exists():
            return render(request, 'crear_usuario.html', {
                'error': 'El correo ya está registrado'
            })

        usuario = Usuario.objects.create(
            nombre=nombre,
            email=email
        )

        return redirect('dashboard', usuario_id=usuario.id)

    return render(request, 'crear_usuario.html')


# EDITAR USUARIO
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        email = request.POST['email']

        # 🔥 validar email duplicado
        if Usuario.objects.filter(email=email).exclude(id=usuario.id).exists():
            return render(request, 'editar_usuario.html', {
                'usuario': usuario,
                'error': 'El correo ya está registrado'
            })

        # ✅ SOLO se actualiza el email
        usuario.email = email
        usuario.save()

        return redirect('dashboard', usuario_id=usuario.id)

    return render(request, 'editar_usuario.html', {
        'usuario': usuario
    })


# ELIMINAR USUARIO
def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    return redirect('lista_usuarios')


# CREAR TRANSACCIÓN 🔥
def crear_transaccion(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        monto = Decimal(request.POST['monto'])
        tipo = request.POST['tipo']

        if tipo == 'deposito':
            usuario.saldo += monto

        elif tipo == 'retiro':
            if usuario.saldo >= monto:
                usuario.saldo -= monto
            else:
                return render(request, 'error.html', {
                    'mensaje': 'Saldo insuficiente'
                })

        usuario.save()

        Transaccion.objects.create(
            usuario=usuario,
            monto=monto,
            tipo=tipo
        )

        return redirect('dashboard', usuario_id=usuario.id)

    return render(request, 'crear_transaccion.html', {'usuario': usuario})

# LISTA DE USUARIOS
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios})