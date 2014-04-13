require 'test_helper'

class HomeControllerTest < ActionController::TestCase
  test "should get signup" do
    get :signup
    assert_response :success
  end

  test "should get login" do
    get :login
    assert_response :success
  end

  test "should get download" do
    get :download
    assert_response :success
  end

end
