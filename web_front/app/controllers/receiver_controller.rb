class ReceiverController < ApplicationController
  def photo
  	@user = params[:username]
  	@pass = params[:password]
  	@photo = params[:photo]
  	@video = params[:video]
  end
end
