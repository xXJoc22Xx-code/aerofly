{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/xXJoc22Xx-code/aerofly/blob/main/Untitled3.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "2YGk03Z35A_2"
      },
      "outputs": [],
      "source": [
        "!pip install -q streamlit"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "g4nTXYiF5Bn1",
        "outputId": "aeab01bf-70ce-40fa-d152-27ca0f63b064"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Writing app.py\n"
          ]
        }
      ],
      "source": [
        "%%writefile app.py\n",
        "import streamlit as st\n",
        "import uuid\n",
        "\n",
        "class Nota:\n",
        "    def __init__(self, titulo, contenido):\n",
        "        self.id = str(uuid.uuid4())\n",
        "        self.titulo = titulo\n",
        "        self.contenido = contenido\n",
        "\n",
        "    def mostrar(self):\n",
        "        return f\"Título: {self.titulo}\\nContenido: {self.contenido}\"\n",
        "\n",
        "class NotaTexto(Nota):\n",
        "    def mostrar(self):\n",
        "        return f\" {self.contenido}\"\n",
        "\n",
        "class NotaLista(Nota):\n",
        "    def __init__(self, titulo, items):\n",
        "        contenido = \"\\n\".join(f\"- {item}\" for item in items)\n",
        "        super().__init__(titulo, contenido)\n",
        "        self.items = items\n",
        "\n",
        "    def mostrar(self):\n",
        "        return f\"\\n\".join(f\"- {item}\" for item in self.items)\n",
        "\n",
        "class NotaImagen(Nota):\n",
        "    def __init__(self, titulo, url_imagen, descripcion=\"\"):\n",
        "        super().__init__(titulo, descripcion)\n",
        "        self.url_imagen = url_imagen\n",
        "\n",
        "    def mostrar(self):\n",
        "        st.image(self.url_imagen, caption=self.titulo, use_container_width=True)\n",
        "        return f\"Descripción: {self.contenido}\"\n",
        "\n",
        "class BlocDeNotas:\n",
        "    def __init__(self):\n",
        "        self.notas = {}\n",
        "\n",
        "    def agregar_nota(self, nota):\n",
        "        self.notas[nota.id] = nota\n",
        "\n",
        "    def obtener_notas(self):\n",
        "        return list(self.notas.values())\n",
        "\n",
        "    def buscar_por_titulo(self, titulo):\n",
        "        return [nota for nota in self.notas.values() if titulo.lower() in nota.titulo.lower()]\n",
        "\n",
        "    def eliminar_nota(self, id_nota):\n",
        "        if id_nota in self.notas:\n",
        "            del self.notas[id_nota]\n",
        "            return True\n",
        "        return False\n",
        "\n",
        "def main():\n",
        "    st.title(\"📒 Bloc de Notas\")\n",
        "\n",
        "    if 'bloc' not in st.session_state:\n",
        "        st.session_state.bloc = BlocDeNotas()\n",
        "\n",
        "    st.sidebar.header(\"Menu\")\n",
        "    opcion = st.sidebar.selectbox(\n",
        "        \"Seleccione una operación\",\n",
        "        [\"Crear nota\", \"Mostrar notas\", \"Buscar nota\", \"Eliminar nota\"]\n",
        "    )\n",
        "\n",
        "    if opcion == \"Crear nota\":\n",
        "        st.header(\"Crear nueva nota\")\n",
        "        tipo_nota = st.selectbox(\"Tipo de nota\", [\"Texto\", \"Lista\", \"Imagen\"])\n",
        "        titulo = st.text_input(\"Título de la nota*\", help=\"Campo obligatorio\")\n",
        "\n",
        "        if tipo_nota == \"Texto\":\n",
        "            contenido = st.text_area(\"Contenido de la nota\")\n",
        "            if st.button(\"Guardar nota de texto\") and titulo:\n",
        "                st.session_state.bloc.agregar_nota(NotaTexto(titulo, contenido))\n",
        "                st.success(\"✅ Nota de texto guardada!\")\n",
        "\n",
        "        elif tipo_nota == \"Lista\":\n",
        "            items_text = st.text_area(\"Elementos de la lista (uno por línea)\")\n",
        "            items = [item.strip() for item in items_text.split('\\n') if item.strip()]\n",
        "            if st.button(\"Guardar nota de lista\") and titulo and items:\n",
        "                st.session_state.bloc.agregar_nota(NotaLista(titulo, items))\n",
        "                st.success(\"✅ Nota de lista guardada!\")\n",
        "\n",
        "        elif tipo_nota == \"Imagen\":\n",
        "            url_imagen = st.text_input(\"URL de la imagen*\", help=\"Ejemplo: https://ejemplo.com/imagen.jpg\")\n",
        "            descripcion = st.text_area(\"Descripción de la imagen\")\n",
        "            if st.button(\"Guardar nota de imagen\") and titulo and url_imagen:\n",
        "                try:\n",
        "                    # Verificación básica de URL\n",
        "                    if url_imagen.startswith(('http://', 'https://')):\n",
        "                        st.session_state.bloc.agregar_nota(NotaImagen(titulo, url_imagen, descripcion))\n",
        "                        st.success(\"✅ Nota de imagen guardada!\")\n",
        "                    else:\n",
        "                        st.error(\"⚠️ La URL debe comenzar con http:// o https://\")\n",
        "                except Exception as e:\n",
        "                    st.error(f\"Error al procesar la imagen: {str(e)}\")\n",
        "\n",
        "    elif opcion == \"Mostrar notas\":\n",
        "        st.header(\"Todas las notas\")\n",
        "        notas = st.session_state.bloc.obtener_notas()\n",
        "\n",
        "        if not notas:\n",
        "            st.info(\"ℹ️ No hay notas creadas aún\")\n",
        "        else:\n",
        "            for nota in notas:\n",
        "                st.subheader(nota.titulo)\n",
        "                if isinstance(nota, NotaImagen):\n",
        "                    st.write(nota.contenido)  # Descripción\n",
        "                    nota.mostrar()  # Esto muestra la imagen\n",
        "                else:\n",
        "                    st.write(nota.mostrar())\n",
        "                st.write(\"---\")\n",
        "\n",
        "    elif opcion == \"Buscar nota\":\n",
        "        st.header(\"Buscar nota por título\")\n",
        "        busqueda = st.text_input(\"Ingrese parte del título a buscar\")\n",
        "\n",
        "        if st.button(\"🔍 Buscar notas\"):\n",
        "            if busqueda:\n",
        "                resultados = st.session_state.bloc.buscar_por_titulo(busqueda)\n",
        "                if resultados:\n",
        "                    st.success(f\"🔎 Se encontraron {len(resultados)} notas:\")\n",
        "                    for nota in resultados:\n",
        "                        st.subheader(nota.titulo)\n",
        "                        if isinstance(nota, NotaImagen):\n",
        "                            st.write(nota.contenido)\n",
        "                            nota.mostrar()  # Muestra la imagen\n",
        "                        else:\n",
        "                            st.write(nota.mostrar())\n",
        "                        st.write(\"---\")\n",
        "                else:\n",
        "                    st.warning(\"⚠️ No se encontraron notas con ese título\")\n",
        "            else:\n",
        "                st.warning(\"⚠️ Por favor ingrese un término de búsqueda\")\n",
        "\n",
        "    elif opcion == \"Eliminar nota\":\n",
        "        st.header(\"Eliminar nota\")\n",
        "        notas = st.session_state.bloc.obtener_notas()\n",
        "\n",
        "        if notas:\n",
        "            nota_a_eliminar = st.selectbox(\n",
        "                \"Seleccione una nota para eliminar\",\n",
        "                options=notas,\n",
        "                format_func=lambda nota: nota.titulo\n",
        "            )\n",
        "\n",
        "            if st.button(\"🗑️ Eliminar nota seleccionada\"):\n",
        "                if st.session_state.bloc.eliminar_nota(nota_a_eliminar.id):\n",
        "                    st.success(f\"✅ Nota '{nota_a_eliminar.titulo}' eliminada!\")\n",
        "                    st.experimental_rerun()  # Actualiza la lista inmediatamente\n",
        "                else:\n",
        "                    st.error(\"❌ Error al eliminar la nota\")\n",
        "        else:\n",
        "            st.info(\"ℹ️ No hay notas para eliminar\")\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    main()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "w37yTFC95D8_",
        "outputId": "1e7d140c-78e8-4623-b0e0-05c911308d79"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "\u001b[1G\u001b[0K⠙\u001b[1G\u001b[0K⠹\u001b[1G\u001b[0K⠸\u001b[1G\u001b[0K⠼\u001b[1G\u001b[0K⠴\u001b[1G\u001b[0K⠦\u001b[1G\u001b[0K⠧\u001b[1G\u001b[0K⠇\u001b[1G\u001b[0K⠏\u001b[1G\u001b[0K⠋\u001b[1G\u001b[0K⠙\u001b[1G\u001b[0K⠹\u001b[1G\u001b[0K⠸\u001b[1G\u001b[0K⠼\u001b[1G\u001b[0K⠴\u001b[1G\u001b[0K⠦\u001b[1G\u001b[0K⠧\u001b[1G\u001b[0K⠇\u001b[1G\u001b[0K⠏\u001b[1G\u001b[0K⠋\u001b[1G\u001b[0K⠙\u001b[1G\u001b[0K⠹\u001b[1G\u001b[0K⠸\u001b[1G\u001b[0K⠼\u001b[1G\u001b[0K⠴\u001b[1G\u001b[0K⠦\u001b[1G\u001b[0K⠧\u001b[1G\u001b[0K⠇\u001b[1G\u001b[0K\n",
            "added 22 packages in 3s\n",
            "\u001b[1G\u001b[0K⠇\u001b[1G\u001b[0K\n",
            "\u001b[1G\u001b[0K⠇\u001b[1G\u001b[0K3 packages are looking for funding\n",
            "\u001b[1G\u001b[0K⠇\u001b[1G\u001b[0K  run `npm fund` for details\n",
            "\u001b[1G\u001b[0K⠇\u001b[1G\u001b[0K"
          ]
        }
      ],
      "source": [
        "!npm install localtunnel"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "background_save": true,
          "base_uri": "https://localhost:8080/"
        },
        "id": "L_pigKpr5FxH",
        "outputId": "c933a8bf-ea79-45e7-975c-69f1132a6304"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "35.239.174.71\n",
            "\u001b[1G\u001b[0K⠙\u001b[1G\u001b[0Kyour url is: https://olive-falcons-sip.loca.lt\n"
          ]
        }
      ],
      "source": [
        "!streamlit run app.py &>/content/logs.txt & npx localtunnel --port 8501 & curl ipv4.icanhazip.com"
      ]
    }
  ],
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyP0jngttZGgAui8tSPmL/8O",
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}
