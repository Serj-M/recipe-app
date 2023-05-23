<template>
  <v-data-table-server 
    v-model:items-per-page="itemsPerPage" 
    :search="search"
    :headers="headers"
    :items-length="totalItems" 
    :items="serverItems" 
    :loading="loading"
    class="elevation-1" 
    item-value="title"
    @update:options="loadItems">
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>Recipe book</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialogAction" max-width="1000px">
          <template v-slot:activator="{ props }">
            <v-btn color="primary" dark class="mb-2" v-bind="props">
              New recipe
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="text-h5">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.title" label="title"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.ingredients" label="ingredients"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.instructions" label="instructions for preparation"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.time" label="Cook time"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.tags" label="Tags"></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue-darken-1" variant="text" @click="close">
                Cancel
              </v-btn>
              <v-btn color="blue-darken-1" variant="text" @click="save">
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="1000px">
          <v-card>
            <v-card-title class="text-h5">Are you sure you want to delete this recipes?</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue-darken-1" variant="text" @click="closeDelete">Cancel</v-btn>
              <v-btn color="blue-darken-1" variant="text" @click="deleteItemConfirm">OK</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <a href="#" class="link-style" @click="editItem(item.raw)">
        Edit
      </a>
      <a href="#" class="link-style" @click="deleteItem(item.raw)">
        Delete
      </a>
    </template>
    <template v-slot:no-data>
      <p>No data</p>
    </template>
    <template v-slot:thead v-if="headers.length">
      <tr>
        <td></td>
        <td>
          <v-text-field v-model="ingredients" hide-details placeholder="Search by ingredient" density="compact"></v-text-field>
        </td>
        <td></td>
        <td></td>
        <td>
          <v-autocomplete v-model="tags" chips label="Search by tags" :items="['Breakfast', 'Lunch', 'Dinner', 'Dessert']"
            multiple></v-autocomplete>
        </td>
      </tr>
    </template>
  </v-data-table-server>
</template>

<script>
import api from '../api'

export default {
  data: () => ({
    paramsLoadItems: {},
    dialogAction: false,
    dialogDelete: false,
    itemsPerPage: 10,
    headers: [],
    serverItems: [],
    loading: false,
    totalItems: 0,
    tags: [],
    ingredients: '',
    search: '',
    editedIndex: -1,
    editedItem: {
      title: '',
      ingredients: '',
      instructions: '',
      time: '',
      tags: '',
    },
    defaultItem: {
      title: '',
      ingredients: '',
      instructions: '',
      time: '',
      tags: '',
    },
  }),

  async created() {
    await this.loadHeaders()
    await this.loadItems({})
  },

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
    },
  },

  watch: {
    title() {
      this.search = String(Date.now())
    },
    ingredients() {
      this.search = String(Date.now())
    },
    dialogAction(val) {
      val || this.close()
    },
    dialogDelete(val) {
      val || this.closeDelete()
    },
  },

  methods: {
    async loadHeaders() {
      try {
        const res = await api.get('/recipes/v1/header')
        this.headers = res.data.headers
      } 
      catch(error) {
        console.error(error)
      }
    },

    async loadItems({ page=1, itemsPerPage=10, sortBy=[] }) {
      this.loading = true
      try {
        this.paramsLoadItems = { 
          page, 
          itemsPerPage, 
          sortBy, 
          search: { tags: this.tags, ingredients: this.ingredients }
        }
        const res = await api.post('/recipes/v1/items', this.paramsLoadItems)
        res.data.items.forEach(el => el.tags = el.tags.join(', '))
        this.serverItems = res.data.items
        this.totalItems = res.data.totalItems
        this.loading = false
      } 
      catch(error) {
        this.loading = false
        console.error(error)
      }
    },

    async editItem(item) {
      this.editedIndex = this.serverItems.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogAction = true
      this.loading = true
      try {
        const id = item.id
        delete item.id
        const params = await this.prepParams(item)
        await api.put(`/recipes/v1/edit/${id}`, params)
        await this.loadItems(this.paramsLoadItems)
        this.loading = false
      } 
      catch(error) {
        this.loading = false
        console.error(error)
      }
    },

    async prepParams(params) {
      const res = await api.get('/recipes/v1/tags')
      const tagsJSON = res.data.tags
      const tagsParams = Array.isArray(params.tags) ? params.tags : params.tags.split(', ')
      const tagIds = tagsParams.map(el => tagsJSON.find(t => t.name == el)?.id)
      params.tags = tagIds
      return params
    },

    deleteItem(item) {
      this.editedIndex = this.serverItems.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },

    deleteItemConfirm() {
      this.serverItems.splice(this.editedIndex, 1)
      this.closeDelete()
    },

    close() {
      this.dialogAction = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    closeDelete() {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.serverItems[this.editedIndex], this.editedItem)
      } else {
        this.serverItems.push(this.editedItem)
      }
      this.close()
    },
  },
}
</script>