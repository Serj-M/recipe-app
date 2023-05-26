<template>
  <v-alert v-if="isDeleted" type="info" variant="outlined" dismissible>
    Recipe successfully deleted
  </v-alert>
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
        <v-toolbar-title class="title-table">titleTable</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialogAction" max-width="1000px">
          <template v-slot:activator="{ props }">
            <v-btn color="blue-darken-1" variant="outlined" class="mb-2" v-bind="props">
              New recipe
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="text-h5">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <p>* required fields</p>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="12" md="6">
                    <v-text-field v-model="editedItem.title" label="title*" :rules="isRequired"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="6">
                    <v-text-field v-model="editedItem.ingredients" label="ingredients*" :rules="isRequired"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="12">
                    <v-textarea v-model="editedItem.instructions" label="instructions for preparation*" :rules="isRequired"></v-textarea>
                  </v-col>
                  <v-col cols="12" sm="12" md="6">
                    <v-text-field v-model="editedItem.time" type="number" label="Cook time*" :rules="numberRules"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="6">
                    <v-autocomplete 
                      v-model="editedItem.tags" 
                      class="mb-0" 
                      chips 
                      label="Tags*" 
                      :items="tagsNames"
                      multiple
                      :rules="isRequiredTags"
                    />
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue-darken-1" variant="text" @click="close">
                Cancel
              </v-btn>
              <v-btn 
                color="blue-darken-1" 
                variant="text" 
                @click="save" 
                :disabled="
                  !editedItem.title || 
                  !editedItem.ingredients || 
                  !editedItem.instructions || 
                  !editedItem.time || parseInt(editedItem.time, 10) < 1 || !/^\d+$/.test(editedItem.time) ||
                  !editedItem.tags.length"
              >
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
      <v-btn color="blue-darken-1" variant="text" density="compact" size="small" @click="editItem(item.raw)">
        Edit
      </v-btn>
      <v-btn color="blue-darken-1" variant="text" density="compact" size="small" @click="deleteItem(item.raw)">
        Delete
      </v-btn>
    </template>
    <template v-slot:no-data>
      <p>No data</p>
    </template>
    <template v-slot:thead v-if="headers.length">
      <tr>
        <td></td>
        <td>
          <v-text-field v-model="ingredients" class="mb-6" hide-details placeholder="Search by ingredient" clearable></v-text-field>
        </td>
        <td></td>
        <td></td>
        <td>
          <v-autocomplete 
            v-model="tags" 
            class="mb-0" 
            chips 
            label="Search by tags" 
            :items="tagsNames"
            multiple
            clearable
          />
        </td>
      </tr>
    </template>
  </v-data-table-server>
</template>

<script>
import api from '../api'

export default {
  data: () => ({
    titleTable: 'Recipes',
    numberRules: [
      value => /^\d+$/.test(value) || 'Enter the correct cooking time (integer only)',
      value => parseInt(value, 10) !== 0 || 'Cooking time cannot be zero',
    ],
    isRequired: [
      value => value !== '' || 'This field is required',
    ],
    isRequiredTags: [
      value => value.length > 0 || 'This field is required',
    ],
    paramsLoadItems: {},
    dialogAction: false,
    dialogDelete: false,
    isDeleted: false,
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
      id: null,
      title: '',
      ingredients: '',
      instructions: '',
      time: '',
      tags: [],
    },
    defaultItem: {
      title: '',
      ingredients: '',
      instructions: '',
      time: '',
      tags: '',
    },
    tagsJSON: [],
    tagsNames: [],
  }),

  async created() {
    await this.loadHeaders()
    await this.loadItems({})
    const res = await api.get('/recipes/v1/tags')
    this.tagsJSON = res.data.tags
    this.tagsNames = this.tagsJSON.map(el => el.name)
  },

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
    },
  },

  watch: {
    tags() {
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
        const tagsIds = this.getTagsIds(this.tags)
        this.paramsLoadItems = { 
          page, 
          itemsPerPage, 
          sortBy, 
          search: { tags: tagsIds, ingredients: this.ingredients }
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

    editItem(item) {
      this.editedIndex = this.serverItems.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.editedItem.tags = this.editedItem.tags.split(', ')
      this.dialogAction = true
    },

    deleteItem(item) {
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },

    async deleteItemConfirm() {
      try {
        const res = await api.delete(`/recipes/v1/del/${this.editedItem.id}`)
        // update recipes to reflect changes
        await this.loadItems(this.paramsLoadItems)
        this.closeDelete()
        this.deleteAlert()
      } catch (error) {
        console.error(error)
      }
    },

    close() {
      this.loading = false
      this.dialogAction = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    closeDelete() {
      this.loading = false
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    deleteAlert() {
      this.isDeleted = true
      setTimeout(() => {
        this.isDeleted = false
      }, 2000)
    },

    async save() {
      this.loading = true
      const id = this.editedItem.id
      delete this.editedItem.id
      try {
        const params = this.prepParams(this.editedItem)
        // Edit recipe
        if (this.editedIndex > -1) {
          await api.put(`/recipes/v1/edit/${id}`, params)
        } 
        // Add recipe
        else {
          await api.post(`/recipes/v1/add`, params)
        }
      } catch (error) {
        console.error(error)
      }
      // update recipes to reflect changes
      await this.loadItems(this.paramsLoadItems)
      this.close()
    },

    prepParams(params) {
      params.tags = this.getTagsIds(params.tags)
      return params
    },

    getTagsIds(tags) {
      const _tags = Array.isArray(tags) ? tags : tags.split(', ')
      const result = _tags.map(el => this.tagsJSON.find(t => t.name == el)?.id)
      return result
    }
  },
}
</script>