<template>
  <v-data-table-server v-model:items-per-page="itemsPerPage" :search="search" :headers="headers"
    :items-length="totalItems" :items="serverItems" :loading="loading" class="elevation-1" item-value="title"
    @update:options="loadItems">
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>Recipe book</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialogAction" max-width="500px">
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
              <v-btn color="blue-darken-1" variant="text" @click="closeAction">
                Cancel
              </v-btn>
              <v-btn color="blue-darken-1" variant="text" @click="save">
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
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
    <template v-slot:thead>
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
const recipes = [
  {
    title: 'Pancakes',
    ingredients: 'Flour, Eggs, Milk, Salt, Sugar, Oil',
    instructions: `Mix flour, eggs, milk, salt, and sugar in a bowl until smooth. 
                  Heat and grease a skillet. Pour the batter onto the skillet and cook until golden brown on both sides. 
                  Repeat with the remaining batter. Serve the pancakes with your favorite fillings or toppings.`,
    time: 1,
    tags: 'Breakfast, Dessert',
  },
]

const FakeAPI = {
  async fetch({ page, itemsPerPage, sortBy, search }) {
    return new Promise(resolve => {
      setTimeout(() => {
        const start = (page - 1) * itemsPerPage
        const end = start + itemsPerPage
        const items = recipes.slice().filter(item => {
          if (search.tags.length && !item.tags.toLowerCase().includes(search.tags[0].toLowerCase())) {
            return false
          }

          // eslint-disable-next-line sonarjs/prefer-single-boolean-return
          if (search.ingredients && !(item.ingredients >= Number(search.ingredients))) {
            return false
          }

          return true
        })

        if (sortBy.length) {
          const sortKey = sortBy[0].key
          const sortOrder = sortBy[0].order
          items.sort((a, b) => {
            const aValue = a[sortKey]
            const bValue = b[sortKey]
            return sortOrder === 'desc' ? bValue - aValue : aValue - bValue
          })
        }

        const paginated = items.slice(start, end)

        resolve({ items: paginated, total: items.length })
      }, 500)
    })
  },
}

export default {
  data: () => ({
    dialogAction: false,
    dialogDelete: false,
    itemsPerPage: 5,
    headers: [
      {
        title: 'Title',
        align: 'start',
        sortable: false,
        key: 'title',
      },
      { title: 'Ingredients', key: 'ingredients', align: 'end', sortable: false  },
      { title: 'Instructions for preparation', key: 'instructions', align: 'end', sortable: false },
      { title: 'Cook time', key: 'time', align: 'end' },
      { title: 'Tags', key: 'tags', align: 'end', sortable: false },
      { title: 'Actions', key: 'actions', sortable: false },
    ],
    serverItems: [],
    loading: true,
    totalItems: 0,
    tags: [],
    ingredients: '',
    search: '',
    editedIndex: -1,
    editedItem: {
      title: '',
      ingredients: 0,
      instructions: 0,
      time: 0,
      tags: 0,
    },
    defaultItem: {
      title: '',
      ingredients: 0,
      instructions: 0,
      time: 0,
      tags: 0,
    },
  }),
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
      val || this.closeAction()
    },
    dialogDelete(val) {
      val || this.closeDelete()
    },
  },
  methods: {
    loadItems({ page, itemsPerPage, sortBy }) {
      this.loading = true
      FakeAPI.fetch({ page, itemsPerPage, sortBy, search: { tags: this.tags, ingredients: this.ingredients } })
        .then(({ items, total }) => {
          this.serverItems = items
          this.totalItems = total
          this.loading = false
        })
    },

    editItem(item) {
      this.editedIndex = this.serverItems.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogAction = true
    },

    deleteItem(item) {
      this.editedIndex = this.serverItems.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },

    deleteItemConfirm() {
      this.recipes.splice(this.editedIndex, 1)
      this.closeDelete()
    },

    closeAction() {
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
        Object.assign(this.recipes[this.editedIndex], this.editedItem)
      } else {
        this.recipes.push(this.editedItem)
      }
      this.closeAction()
    },
  },
}
</script>