import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Recipes from '../Recipes.vue'

describe('Recipes', () => {
  it('must be table title', () => {
    const wrapper = mount(Recipes)
    expect(wrapper.vm.titleTable).toBe('Recipes')
  })
})
